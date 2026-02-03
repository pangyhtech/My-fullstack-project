"""
Input: list of entities, list of relations
Output: Dict:{Rel:keywords}

Save: Keywords for each third category
"""
from EL_RC import *
from TuckER_model import *
import torch
from TuckER_model import *
import codecs
import argparse
import os
from tqdm import tqdm
import pickle

relations2text = {}
entities2text = {}

def get_text_dict(file1, file2):
    with codecs.open(file1, 'r', encoding='utf-8') as f1, codecs.open(file2, 'r', encoding='utf-8') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        for line in lines1:
            line = line.strip().split(',')
            if len(line) != 2:
                continue
            entities2text[int(line[1][4:10])-1] = line[0]

        for line in lines2:
            line = line.strip().split(',')
            if len(line) != 2:
                continue
            relations2text[int(line[1][4:8])-1] = line[0]

class Tail_prediction:
    def __init__(self, learning_rate=0.0005, ent_vec_dim=200, rel_vec_dim=200, 
                 num_iterations=500, batch_size=128, decay_rate=0., cuda=False, 
                 input_dropout=0.3, hidden_dropout1=0.4, hidden_dropout2=0.5,
                 label_smoothing=0.):
        self.learning_rate = learning_rate
        self.ent_vec_dim = ent_vec_dim
        self.rel_vec_dim = rel_vec_dim
        self.num_iterations = num_iterations
        self.batch_size = batch_size
        self.decay_rate = decay_rate
        self.label_smoothing = label_smoothing
        self.cuda = cuda
        self.kwargs = {"input_dropout": input_dropout, "hidden_dropout1": hidden_dropout1,
                       "hidden_dropout2": hidden_dropout2}

    def prediction_single_entity(self, model, e1_idx, r_idx_list):
        for r_idx in r_idx_list:
            predictions = model.forward(torch.tensor(e1_idx).to('cpu'), torch.tensor([r_idx*2]).to('cpu'))

            print("Prediction:", entities2text[e1_idx[0]], relations2text[r_idx])

            _, sort_idxs = torch.sort(predictions, dim=1, descending=True)

            sort_idxs = sort_idxs.cpu().numpy()

            print("Predicted tails:")

            for k in range(0, 5):
                print(entities2text[sort_idxs[0][k]])
    
    def get_related_keywords(self, model, related_entities, related_relations):
        rel_index = []
        keyword_dict = {}

        for rel_text in related_relations:
            rel_index.append(int(rel_text[4:]))

        for ent in related_entities:
            ent_index = int(ent[4:])
            for rel in rel_index:
                predictions = model.forward(torch.tensor([ent_index-1]).to('cpu'), torch.tensor([(rel-1)*2]).to('cpu'))
                
                _, sort_idxs = torch.sort(predictions, dim=1, descending=True)
                sort_idxs = sort_idxs.cpu().numpy()
                
                for k in range(0, 5):
                    if relations2text[rel-1] in keyword_dict.keys():
                        keyword_dict[relations2text[rel-1]].append(entities2text[sort_idxs[0][k]])
                    else:
                        keyword_dict[relations2text[rel-1]] = [entities2text[sort_idxs[0][k]]]
        
        for rel in rel_index:
            keyword_dict[relations2text[rel-1]] = list(set(keyword_dict[relations2text[rel-1]]))
        
        return keyword_dict
    
    def get_new_tucker(self, ent_len, rel_len):
        model = TuckER(ent_len, rel_len, self.ent_vec_dim, self.rel_vec_dim, **self.kwargs)
        if self.cuda:
            model.to('cpu')
        return model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="OpenBG500", nargs="?",
                    help="Which dataset to use: FB15k, FB15k-237, WN18 or WN18RR.")
    parser.add_argument("--num_iterations", type=int, default=50, nargs="?",
                    help="Number of iterations.")
    parser.add_argument("--batch_size", type=int, default=1, nargs="?",
                    help="Batch size.")
    parser.add_argument("--lr", type=float, default=0.003, nargs="?",
                    help="Learning rate.")
    parser.add_argument("--dr", type=float, default=0.95, nargs="?",
                    help="Decay rate.")
    parser.add_argument("--edim", type=int, default=200, nargs="?",
                    help="Entity embedding dimensionality.")
    parser.add_argument("--rdim", type=int, default=200, nargs="?",
                    help="Relation embedding dimensionality.")
    parser.add_argument("--cuda", type=bool, default=True, nargs="?",
                    help="Whether to use cuda (GPU) or not (CPU).")
    parser.add_argument("--input_dropout", type=float, default=0.2, nargs="?",
                    help="Input layer dropout.")
    parser.add_argument("--hidden_dropout1", type=float, default=0.2, nargs="?",
                    help="Dropout after the first hidden layer.")
    parser.add_argument("--hidden_dropout2", type=float, default=0.3, nargs="?",
                    help="Dropout after the second hidden layer.")
    parser.add_argument("--label_smoothing", type=float, default=0, nargs="?",
                    help="Amount of label smoothing.")

    args = parser.parse_args()
    
    experiment = Tail_prediction(num_iterations=args.num_iterations, batch_size=args.batch_size, learning_rate=args.lr, 
                            decay_rate=args.dr, ent_vec_dim=args.edim, rel_vec_dim=args.rdim, cuda=args.cuda,
                            input_dropout=args.input_dropout, hidden_dropout1=args.hidden_dropout1, 
                            hidden_dropout2=args.hidden_dropout2, label_smoothing=args.label_smoothing)

    get_text_dict("KG_tail_prediction/data/E&R/entity_examples.csv","KG_tail_prediction/data/E&R/relation_examples.csv")

    new_model = experiment.get_new_tucker(18720, 912)
    new_model.load_state_dict(torch.load("KG_tail_prediction/model/TuckER_model.pkl", map_location='cpu'))
    new_model.eval()

    tc_list = []
    file_folders = {'label_0','label_25','label_50','label_75','label_100'}
    for file_folder in file_folders:
        for i in range(1, 3200):
            file_path = "dialogue_{}.csv".format(i)
            if not os.path.exists(file_path):
                continue
            df = pd.read_csv(file_path)
            third_category = df.iloc[0, 10]
            if third_category not in tc_list:
                tc_list.append(third_category)


    print(len(tc_list))
    final_saved = {}

    for tc in tqdm(tc_list, desc="Processing"):
        related_ent, related_rel = EL_RC(tc)

        if related_ent == None:
            print(tc,"cannot be found")
            continue

        keyword_dict = experiment.get_related_keywords(new_model, related_ent, related_rel)
        final_saved[tc] = keyword_dict
    
    # Save the predicted tails
    with open("keyword_dict.pkl", "wb") as pickle_file:
        pickle.dump(final_saved, pickle_file)
    
