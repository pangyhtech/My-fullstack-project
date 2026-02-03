import pandas as pd
import os
import numpy as np
from torch.nn.utils.rnn import pad_sequence
from transformers import BertTokenizer,BertModel
import torch.optim as optim
from datasets import Dataset
import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F
import torch.nn as nn
from tqdm import tqdm
from utils.transformer import *
import random
from sklearn.metrics import classification_report
import argparse
from torch.optim.lr_scheduler import StepLR

def universal_sentence_embedding(sentences, mask, sqrt=True):
    sentence_sums = torch.bmm(
        sentences.permute(0, 2, 1), mask.float().unsqueeze(-1)
    ).squeeze(-1)
    divisor = mask.sum(dim=1).view(-1, 1).float()
    if sqrt:
        divisor = divisor.sqrt()
    sentence_sums /= divisor
    return sentence_sums

class BaseModelBackbone(nn.Module):
    def __init__(self, **config):
        super().__init__()
        model_name = 'bert-base-chinese'
        self.base_model = BertModel.from_pretrained(model_name)
        self.d_model = self.base_model.config.hidden_size

    def forward(self, input_ids):
        attention_mask = input_ids.ne(0).detach()
        outputs = self.base_model(input_ids, attention_mask)
        h = universal_sentence_embedding(outputs.last_hidden_state, attention_mask)
        cls = outputs.pooler_output

        out = torch.cat([cls, h], dim=-1)
        return out

class MLP(nn.Module):
    def __init__(self, input_size, output_size, hidden_size, dropout=0.1):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, din):
        dout = self.dropout(F.relu(self.fc1(din)))
        dout = self.fc2(dout)
        return dout

class CSP_Classifier(nn.Module):
    def __init__(self, text_base_model_name, keyword_base_model,heads, layers, dropout, topic_num, sat_num=5):
        super(CSP_Classifier, self).__init__()
        self.turn_encoder = BaseModelBackbone(model_name=text_base_model_name)
        self.keyword_encoder = keyword_base_model
        d_model = self.turn_encoder.d_model
        self.dialogue_encoder = TransformerEncoder(d_model*2, d_model*4, heads, layers, dropout)
        self.layer_norm = nn.LayerNorm(d_model*2, eps=1e-6)
        self.dim_reduction = nn.Linear(d_model*2, d_model)
        self.topic_embedding = nn.Embedding(topic_num, 768)
        self.atten_QA = nn.MultiheadAttention(1, 1, batch_first=True)
        self.atten_Topic = nn.MultiheadAttention(768, 6, batch_first=True)
        self.atten_Keyword = nn.MultiheadAttention(768, 6, batch_first=True)

        self.sat_num = sat_num
        self.sat_pred = MLP(d_model*4, sat_num, d_model//4)

        self.dropout = nn.Dropout(0.1)


    def forward(self, input_ids, Q_keywords, A_keywords, topic, mask):
        # Get basic information
        batch_size, dialog_len, utt_len = input_ids.size()
        d_model = self.turn_encoder.d_model

        # Turn level encode
        input_ids = input_ids.view(-1, utt_len)
        turn_embedding = self.turn_encoder(input_ids=input_ids)
        turn_embedding = turn_embedding.view(batch_size, dialog_len, -1)
        
        # Dialogue level encode
        attention_mask = mask.unsqueeze(-2).repeat(1, dialog_len, 1)
        attention_mask &= subsequent_mask(dialog_len).to(input_ids.device)
        dial_out = self.dialogue_encoder(turn_embedding, attention_mask)
        
        dial_out = self.layer_norm(dial_out)
        dial_out = self.dim_reduction(dial_out)
        dial_out = self.dropout(dial_out)
        
        last_index = torch.sum(mask, dim=-1, keepdim=True) - 1
        index_matrix = last_index[:, :, None].expand(-1, -1, dial_out.size(-1))
        dialogue_embedding = torch.gather(dial_out, 1, index_matrix)
        dialogue_embedding = dialogue_embedding.view(batch_size, -1)

        # Q\A encode
        attention_mask_Q = Q_keywords.ne(0).detach()
        Q_output = self.keyword_encoder(input_ids=Q_keywords, attention_mask=attention_mask_Q)
        Q_embeddings = Q_output[1]

        attention_mask_A = A_keywords.ne(0).detach()
        A_output = self.keyword_encoder(input_ids=A_keywords, attention_mask=attention_mask_A)
        A_embeddings = A_output[1]

        # QA emebedding fusion
        QA_embeddings = torch.mean(torch.stack([Q_embeddings, A_embeddings]), dim=0)

        # Dialogue attention
        QA_atten_output, _ = self.atten_QA(Q_embeddings.unsqueeze(2), A_embeddings.unsqueeze(2), A_embeddings.unsqueeze(2))
        QA_atten_output = QA_atten_output.view(batch_size, -1)

        # Keyword attention
        QA_embeddings = QA_embeddings.unsqueeze(1).expand(batch_size, dialog_len, d_model)
        Keyword_atten, _ = self.atten_Keyword(QA_embeddings, dial_out, dial_out)
        Keyword_atten_mean = torch.mean(Keyword_atten, dim=1)

        # Product attention
        topic_embeddings = self.topic_embedding(topic).unsqueeze(1).expand(batch_size, dialog_len, d_model)
        Topic_atten, _ = self.atten_Topic(topic_embeddings, dial_out, dial_out)
        Topic_atten_mean = torch.mean(Topic_atten, dim=1)

        # Concat four feature vectors
        final_vector = torch.cat([dialogue_embedding, QA_atten_output, Keyword_atten_mean, Topic_atten_mean], dim=1)
        
        # Final prediction
        last_sat_logits = self.sat_pred(final_vector)
        
        return last_sat_logits


def preprocess_text(text):
    ids = []
    for sent in text.split('|||'):
        ids += tokenizer.encode(sent)[1:]
        if len(ids) >= max_seq_len-1:
            ids = ids[:max_seq_len-2] + [102]
            break
                    
    return ids

def preprocess_keywords(text):
    encoded_keywords = tokenizer.encode(text, add_special_tokens=False)
    return encoded_keywords

def get_keywords(key_str):
    q_index = key_str.find("Q:")
    a_index = key_str.find("A:")

    q_text = key_str[q_index + 2 : a_index].strip()
    a_text = key_str[a_index + 2 :].strip()

    q_list = q_text.split(";")[0:-1]
    a_list = a_text.split(";")[0:-1]

    if len(q_list) == 0:
        q_list.append("no_token")
    
    if len(a_list) == 0:
        a_list.append("no_token")

    return q_list, a_list

def data_collate(data):
    padded_dialogues = []
    padded_Qs = []
    padded_As = []
    topic = []
    labels = []
    masks = []
    batch_size = len(data)
    
    for i in range(0, len(data)):
        masks.append(data[i]['mask'])
    
    masks = [torch.tensor(item).long() for item in masks]
    masks = pad_sequence(masks, batch_first=True, padding_value=-1)
    dialog_len = len(masks[0])
        
    for i in range(0, len(data)):
        dialog = data[i]['dialogue']

        x = dialog + [[101, 102]] * (dialog_len - len(dialog))
        padded_dialogues.append(x)

        padded_Q = []
        for Q_keyword in data[i]['Q_keywords']:
            padded_Q.extend(Q_keyword)
            padded_Q.append(tokenizer.sep_token_id)
        if len(padded_Q) > max_length -1 :
            padded_Q = padded_Q[-max_length+1:]
        padded_Q = [tokenizer.cls_token_id] + padded_Q

        padded_A = []
        for A_keyword in data[i]['A_keywords']:
            padded_A.extend(A_keyword)
            padded_A.append(tokenizer.sep_token_id)
        if len(padded_A) > max_length -1 :
            padded_A = padded_A[-max_length+1:]
        padded_A = [tokenizer.cls_token_id] + padded_A

        padded_Qs.append(padded_Q)
        padded_As.append(padded_A)
        topic.append(data[i]['topic'])
        labels.append(data[i]['label'])

    input_ids = [torch.tensor(item).long() for dialog in padded_dialogues for item in dialog]
    input_ids = pad_sequence(input_ids, batch_first=True, padding_value=0)
    input_ids = input_ids.view(batch_size, dialog_len, -1)

    input_Qs = [torch.tensor(Q).long() for Q in padded_Qs]
    input_Qs = pad_sequence(input_Qs, batch_first=True, padding_value=0)

    input_As = [torch.tensor(A).long() for A in padded_As]
    input_As = pad_sequence(input_As, batch_first=True, padding_value=0)
    
    topic = torch.tensor(topic).long()
    labels = torch.tensor(labels).long()
    
    return {
        'input_ids':input_ids,
        'Q_keywords':input_Qs,
        'A_keywords':input_As,
        'topic':topic,
        'labels':labels,
        'mask':masks.ne(-1)        
    }

def load_data():
    valid_data = {"dialogue": [], "topic": [],"label": [], "Q_keywords":[], "A_keywords":[], "mask":[]}
    train_data = {"dialogue": [], "topic": [],"label": [], "Q_keywords":[], "A_keywords":[], "mask":[]}
    
    valid_data_path = 'path_to_data/valid/data_turn/dialogue_{}.csv'
    train_data_path = 'path_to_data/train/data_turn/dialogue_{}.csv'
    
    start_index = 0
    
    for i in tqdm(range(1, 6000)):
        file_path = train_data_path.format(i)
        if not os.path.exists(file_path):
            continue
        df = pd.read_csv(file_path)
        topic = 0
        keywords = df["keywords"][0]
        first_topic = df["first_category"][0]

        if first_topic in topic_index.keys():
            topic = topic_index[first_topic]
        else:
            topic_index[first_topic] = start_index
            topic = start_index
            start_index += 1

        Q_list, A_list = get_keywords(keywords)
        processed_Q_keywords = [preprocess_keywords(Q_text) for Q_text in Q_list]
        processed_A_keywords = [preprocess_keywords(A_text) for A_text in A_list]
        processed_dialogue = [preprocess_text(dialogue) for dialogue in df["sent"]]
        dialogue_label = int(df["sat"].tolist()[0])
        train_data["Q_keywords"].append(processed_Q_keywords)
        train_data["A_keywords"].append(processed_A_keywords)
        train_data["dialogue"].append(processed_dialogue)
        train_data["topic"].append(topic)
        train_data['mask'].append(list(np.arange(len(df['sent']))))
        train_data["label"].append(dialogue_label)
    
    for i in tqdm(range(1, 1000)):
        file_path = valid_data_path.format(i)
        if not os.path.exists(file_path):
            continue
        df = pd.read_csv(file_path)
        topic = 0
        keywords = df["keywords"][0]
        first_topic = df["first_category"][0]

        if first_topic in topic_index.keys():
            topic = topic_index[first_topic]
        else:
            topic_index[first_topic] = start_index
            topic = start_index
            start_index += 1

        Q_list, A_list = get_keywords(keywords)
        processed_Q_keywords = [preprocess_keywords(Q_text) for Q_text in Q_list]
        processed_A_keywords = [preprocess_keywords(A_text) for A_text in A_list]
        processed_dialogue = [preprocess_text(dialogue) for dialogue in df["sent"]]
        dialogue_label = int(df["sat"].tolist()[0])
        valid_data["Q_keywords"].append(processed_Q_keywords)
        valid_data["A_keywords"].append(processed_A_keywords)
        valid_data["dialogue"].append(processed_dialogue)
        valid_data["topic"].append(topic)
        valid_data['mask'].append(list(np.arange(len(df['sent']))))
        valid_data["label"].append(dialogue_label)
    
    train_data = Dataset.from_dict(train_data)
    valid_data = Dataset.from_dict(valid_data)

    train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True, collate_fn=data_collate)
    valid_dataloader = DataLoader(valid_data, batch_size=1, shuffle=True, collate_fn=data_collate)
    return train_dataloader, valid_dataloader

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True

if __name__ == '__main__':
    batch_size = 8
    max_seq_len = 64
    max_length = 512
    dropout = 0.1
    sat_num = 5
    seed = 42
    topic_index = {}
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--layers", default=3, type=int,
                    help="Number of transformer layers.")
    parser.add_argument("--heads", default=12, type=int,
                    help="Number of transformer heads.")

    args = parser.parse_args()
    
    layers = args.layers
    heads = args.heads
    

    print('layers', args.layers)
    print('heads', args.heads)
    
    with open("exp_outputs.txt", "a") as file:
        file.write("***** CoRe-USE training *****\n")
        file.write("TF_heads:{}\n".format(heads))
        file.write("TF_layers:{}\n".format(layers))
        file.write("Seed:{}\n".format(seed))

    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    new_tokens = ['no_token']
    num_added_toks = tokenizer.add_tokens(new_tokens)

    backbone_model = BertModel.from_pretrained('bert-base-chinese')
    backbone_model.resize_token_embeddings(len(tokenizer))

    descriptions = ['空无没']
    with torch.no_grad():
        for i, token in enumerate(reversed(descriptions), start=1):
            tokenized = tokenizer.tokenize(token)
            tokenized_ids = tokenizer.convert_tokens_to_ids(tokenized)
            new_embedding = backbone_model.embeddings.word_embeddings.weight[tokenized_ids].mean(axis=0)
            backbone_model.embeddings.word_embeddings.weight[-i, :] = new_embedding.clone().detach().requires_grad_(True)
    
    backbone_model_text = BertModel.from_pretrained('bert-base-chinese')
    
    set_seed(seed)

    backbone = backbone_model
    train_dataloader, valid_dataloader = load_data()
    model = CSP_Classifier(text_base_model_name='bert-base-chinese', keyword_base_model=backbone_model, topic_num=len(topic_index), heads=heads, layers=layers, dropout=dropout, sat_num=sat_num).to('cuda:0')

    optimizer = optim.Adam(model.parameters(), lr=1e-5)
    scheduler = StepLR(optimizer, step_size=4, gamma=0.5)
    num_epochs = 10
    avg_res = 0

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for batch in tqdm(train_dataloader, desc='Training', leave=True):
            dialogues = batch['input_ids'].to('cuda')
            Q_keywords = batch['Q_keywords'].to('cuda')
            A_keywords = batch['A_keywords'].to('cuda')
            topic = batch['topic'].to('cuda')
            labels = batch['labels'].to('cuda')
            mask = batch['mask'].to('cuda')

            optimizer.zero_grad()

            res = model(dialogues, Q_keywords, A_keywords, topic, mask)
            loss = F.cross_entropy(res, labels)
            
            loss.backward()
            optimizer.step()

            total_loss += torch.sum(loss)
        
        scheduler.step()
        model.eval()

        predictions = []
        test_labels = []
        for batch in tqdm(valid_dataloader, desc='Testing', leave=True):
            dialogues = batch['input_ids'].to('cuda')
            Q_keywords = batch['Q_keywords'].to('cuda')
            A_keywords = batch['A_keywords'].to('cuda')
            topic = batch['topic'].to('cuda')
            labels = batch['labels']
            mask = batch['mask'].to('cuda')
            res = model(dialogues, Q_keywords, A_keywords, topic, mask)
            _, predicted = torch.max(res, dim=1)
            predictions.append(predicted.item())
            test_labels.append(labels.item())
        report = classification_report(test_labels, predictions, digits=4)
        
        lines = report.split('\n')
        metric_name_1, metric_name_2, precision, recall, f1_score, support = lines[9].split()
        res_1 = float(precision)
        res_2 = float(recall)
        res_3 = float(f1_score)
   
        if (res_1 + res_2 +res_3) / 3 > avg_res:
            avg_res = (res_1 + res_2 +res_3) / 3
            torch.save(model, 'model_hub/CoRe-USE_heads{}_layers{}_seed{}.pth'.format(heads, layers, seed))
        
        with open("exp_outputs.txt", "a") as file:
            file.write("Epoch:{}\n".format(epoch))
            file.write(report)
            file.write("END REPORT\n")

    


