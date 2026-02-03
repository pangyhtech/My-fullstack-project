# -*- coding: utf-8 -*-
"""
MonotaRO 版 run_full_pipeline.py (高精度版 v2)
目標: データ拡張 + 大規模事前学習モデル

主な改善点:
1. XLM-RoBERTa (多言語対応、2.7億パラメータ)
2. データ拡張 (同義語置換、ランダム削除)
3. Focal Loss (クラス不均衡対策)
4. 3クラス分類 (不満/普通/満足)
"""

import sys
import os
import pandas as pd
import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, WeightedRandomSampler
from torch.nn.utils.rnn import pad_sequence
from tqdm import tqdm
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
import numpy as np
import random
import re

# Setup
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
monotaro_dir = os.path.dirname(current_dir)

sys.path.insert(0, root_dir)
sys.path.insert(0, monotaro_dir)
sys.path.insert(0, os.path.join(monotaro_dir, "KG_tail_prediction"))
sys.path.insert(0, current_dir)

from monotaro_categories import CATEGORY_ENTITIES, CATEGORY_LIST

# ==========================================
# Config (高精度版 v2)
# ==========================================
BATCH_SIZE = 16          # 削減: XLM-RoBERTaは大きいため
EPOCHS = 15              
LR = 3e-5                
WARMUP_RATIO = 0.1
DEVICE = 'cpu'
PATIENCE = 5             
NUM_CLASSES = 3          
USE_DATA_AUGMENTATION = True

print("=" * 60)
print(" MonotaRO High-Accuracy Pipeline v2")
print(" (Data Augmentation + XLM-RoBERTa)")
print("=" * 60)

# ==========================================
# Load Model (XLM-RoBERTa or fallback)
# ==========================================
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup

try:
    print(">>> Loading XLM-RoBERTa (270M parameters)...")
    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
    MODEL_NAME = "xlm-roberta-base"
except Exception as e:
    print(f">>> XLM-RoBERTa not available, falling back...")
    try:
        tokenizer = AutoTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-v2")
        MODEL_NAME = "cl-tohoku/bert-base-japanese-v2"
    except:
        tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
        MODEL_NAME = "bert-base-multilingual-cased"

print(f">>> Using model: {MODEL_NAME}")
tokenizer.add_special_tokens({'additional_special_tokens': ['[NO_TOKEN]']})

# ==========================================
# Data Augmentation / データ拡張
# ==========================================

# 日本語同義語辞書
JA_SYNONYMS = {
    "いくら": ["何円", "価格は", "おいくら", "いくらですか"],
    "在庫": ["ストック", "入荷", "品物"],
    "納期": ["お届け", "発送", "配送"],
    "保証": ["ワランティ", "保証書", "保証期間"],
    "返品": ["返却", "キャンセル", "返金"],
    "買う": ["購入", "注文", "オーダー"],
    "高い": ["高価", "お高め", "値が張る"],
    "安い": ["お得", "リーズナブル", "お手頃"],
    "大丈夫": ["問題ない", "OK", "オーケー"],
    "ありがとう": ["サンキュー", "感謝", "助かります"],
    "すみません": ["ごめんなさい", "申し訳", "お手数"],
    "わかりました": ["了解", "承知", "理解しました"],
}

def synonym_replace(text, prob=0.15):
    """同義語置換"""
    words = text.split()
    for i, word in enumerate(words):
        for key, synonyms in JA_SYNONYMS.items():
            if key in word and random.random() < prob:
                words[i] = word.replace(key, random.choice(synonyms))
                break
    return " ".join(words)

def random_deletion(text, prob=0.1):
    """ランダム削除"""
    # 区切り文字で分割
    parts = re.split(r'(\|\|\|)', text)
    result = []
    for part in parts:
        if part == '|||':
            result.append(part)
        else:
            words = list(part)
            # 10%の確率で文字を削除（文が短くなりすぎないように）
            if len(words) > 5 and random.random() < 0.5:
                new_words = [w for w in words if random.random() > prob]
                result.append(''.join(new_words) if len(new_words) > 3 else part)
            else:
                result.append(part)
    return ''.join(result)

def random_swap(text, n=2):
    """ランダム入れ替え"""
    # ターン単位で入れ替えは破壊的なので、文字レベルで軽微に
    chars = list(text)
    if len(chars) < 10:
        return text
    for _ in range(n):
        i, j = random.sample(range(len(chars)), 2)
        if chars[i] not in '|||QA:' and chars[j] not in '|||QA:':
            chars[i], chars[j] = chars[j], chars[i]
    return ''.join(chars)

def augment_text(text):
    """テキスト拡張"""
    if not USE_DATA_AUGMENTATION:
        return text
    
    augmented = text
    
    # 30%の確率で同義語置換
    if random.random() < 0.3:
        augmented = synonym_replace(augmented)
    
    # 20%の確率でランダム削除
    if random.random() < 0.2:
        augmented = random_deletion(augmented)
    
    return augmented

# ==========================================
# Data Processing
# ==========================================

def sat_to_3class(sat):
    if sat <= 2:
        return 0  # 不満
    elif sat <= 4:
        return 1  # 普通
    else:
        return 2  # 満足

def preprocess_text(text, augment=False):
    if augment:
        text = augment_text(text)
    
    # 全ターンを連結
    turns = text.split('|||')
    combined = ' '.join([t.strip() for t in turns if t.strip()])
    
    # トークン化
    encoded = tokenizer.encode(combined, max_length=256, truncation=True)
    return encoded

def run_pipeline_on_row(row, augment=False):
    text = row['sent']
    category = row['first_category']
    original_sat = int(row['sat'])
    
    input_ids = preprocess_text(text, augment=augment)
    
    return {
        "input_ids": input_ids,
        "topic": CATEGORY_LIST.index(category) if category in CATEGORY_LIST else 0,
        "label": sat_to_3class(original_sat),
        "original_label": original_sat
    }

def load_dataset(mode='train'):
    data_list = []
    if mode == 'train':
        file_range = range(1, 51)
        folder = os.path.join(monotaro_dir, "reproduce/data/train/data_turn")
    else:
        file_range = range(1, 6)
        folder = os.path.join(monotaro_dir, "reproduce/data/valid/data_turn")
    
    files = [os.path.join(folder, f"dialogue_{i}.csv") for i in file_range]
    print(f">>> Loading {mode.upper()} data from {len(files)} files...")
    
    for fpath in files:
        if not os.path.exists(fpath):
            continue
        df = pd.read_csv(fpath, encoding='utf-8-sig')
        for _, row in df.iterrows():
            try:
                # 訓練データには拡張を適用
                processed = run_pipeline_on_row(row, augment=(mode == 'train'))
                data_list.append(processed)
            except Exception as e:
                continue
    
    print(f"    -> Loaded {len(data_list)} samples.")
    return data_list

def collate_fn(data):
    input_ids_list = [torch.tensor(d['input_ids']).long() for d in data]
    input_ids = pad_sequence(input_ids_list, batch_first=True, padding_value=tokenizer.pad_token_id or 0)
    attention_mask = (input_ids != (tokenizer.pad_token_id or 0)).long()
    
    topics = torch.tensor([d['topic'] for d in data]).long()
    labels = torch.tensor([d['label'] for d in data]).long()
    
    return input_ids, attention_mask, topics, labels

# ==========================================
# Focal Loss (クラス不均衡対策)
# ==========================================

class FocalLoss(torch.nn.Module):
    def __init__(self, gamma=2.0, alpha=None):
        super().__init__()
        self.gamma = gamma
        self.alpha = alpha
    
    def forward(self, pred, target):
        ce_loss = F.cross_entropy(pred, target, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = ((1 - pt) ** self.gamma) * ce_loss
        
        if self.alpha is not None:
            alpha_t = self.alpha[target]
            focal_loss = alpha_t * focal_loss
        
        return focal_loss.mean()

# ==========================================
# Model (XLM-RoBERTa版)
# ==========================================

class HighAccuracyClassifierV2(torch.nn.Module):
    def __init__(self, backbone, hidden_size=768, topic_num=24, num_classes=3):
        super().__init__()
        self.backbone = backbone
        self.hidden_size = hidden_size
        self.topic_embed = torch.nn.Embedding(topic_num, 128)
        
        # 分類ヘッド
        self.classifier = torch.nn.Sequential(
            torch.nn.Linear(hidden_size + 128, 512),
            torch.nn.LayerNorm(512),
            torch.nn.GELU(),
            torch.nn.Dropout(0.3),
            torch.nn.Linear(512, 256),
            torch.nn.LayerNorm(256),
            torch.nn.GELU(),
            torch.nn.Dropout(0.2),
            torch.nn.Linear(256, num_classes)
        )
        
        # 重み初期化
        for module in self.classifier:
            if isinstance(module, torch.nn.Linear):
                torch.nn.init.xavier_normal_(module.weight)
                torch.nn.init.zeros_(module.bias)
    
    def forward(self, input_ids, attention_mask, topics):
        outputs = self.backbone(input_ids, attention_mask=attention_mask)
        
        # [CLS]トークンの出力
        if hasattr(outputs, 'last_hidden_state'):
            cls_output = outputs.last_hidden_state[:, 0, :]
        else:
            cls_output = outputs[0][:, 0, :]
        
        topic_emb = self.topic_embed(topics)
        combined = torch.cat([cls_output, topic_emb], dim=-1)
        
        logits = self.classifier(combined)
        return logits

# ==========================================
# Main
# ==========================================

if __name__ == "__main__":
    print(f">>> Config: Epochs={EPOCHS}, LR={LR}, Batch={BATCH_SIZE}, Classes={NUM_CLASSES}")
    print(f">>> Data Augmentation: {USE_DATA_AUGMENTATION}")
    print("=" * 60)
    
    print(">>> [1/5] Loading Data...")
    train_data = load_dataset('train')
    valid_data = load_dataset('valid')
    
    if len(train_data) == 0:
        print("!!! No training data found.")
        exit(1)
    
    # ラベル分布
    train_labels = [d['label'] for d in train_data]
    label_counts = [train_labels.count(i) for i in range(NUM_CLASSES)]
    print(f"    Label distribution: 0={label_counts[0]}, 1={label_counts[1]}, 2={label_counts[2]}")
    
    # クラス重み計算 (不均衡対策)
    total = sum(label_counts)
    class_weights = torch.tensor([total / (NUM_CLASSES * c) for c in label_counts]).float()
    print(f"    Class weights: {class_weights.tolist()}")
    
    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
    valid_loader = DataLoader(valid_data, batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate_fn)
    
    print(">>> [2/5] Building Model...")
    try:
        backbone = AutoModel.from_pretrained(MODEL_NAME)
        hidden_size = backbone.config.hidden_size
    except:
        from transformers import BertModel
        backbone = BertModel.from_pretrained("bert-base-multilingual-cased")
        hidden_size = 768
    
    backbone.resize_token_embeddings(len(tokenizer))
    
    # BERT全層を微調整
    for param in backbone.parameters():
        param.requires_grad = True
    
    model = HighAccuracyClassifierV2(backbone, hidden_size=hidden_size, topic_num=24, num_classes=NUM_CLASSES).to(DEVICE)
    
    # Optimizer & Scheduler
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)
    total_steps = len(train_loader) * EPOCHS
    warmup_steps = int(total_steps * WARMUP_RATIO)
    scheduler = get_linear_schedule_with_warmup(optimizer, warmup_steps, total_steps)
    
    # Focal Loss with class weights
    criterion = FocalLoss(gamma=2.0, alpha=class_weights.to(DEVICE))
    
    print(f">>> [3/5] Training for {EPOCHS} epochs (Warmup: {warmup_steps} steps)...")
    
    best_acc = 0
    best_f1 = 0
    patience_counter = 0
    
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        
        for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS}"):
            inp, mask, top, lbl = [b.to(DEVICE) for b in batch]
            
            optimizer.zero_grad()
            logits = model(inp, mask, top)
            loss = criterion(logits, lbl)
            
            if torch.isnan(loss):
                continue
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            total_loss += loss.item()
        
        # Evaluation
        model.eval()
        all_preds, all_trues = [], []
        with torch.no_grad():
            for batch in valid_loader:
                inp, mask, top, lbl = [b.to(DEVICE) for b in batch]
                logits = model(inp, mask, top)
                preds = torch.argmax(logits, dim=1)
                all_preds.extend(preds.cpu().numpy())
                all_trues.extend(lbl.cpu().numpy())
        
        acc = accuracy_score(all_trues, all_preds) * 100
        p, r, f1, _ = precision_recall_fscore_support(all_trues, all_preds, average='macro', zero_division=0)
        
        print(f"    Epoch {epoch+1}: Loss={total_loss:.2f}, Acc={acc:.2f}%, F1={f1*100:.2f}%")
        
        # Early Stopping
        if acc > best_acc:
            best_acc = acc
            best_f1 = f1
            patience_counter = 0
            torch.save(model.state_dict(), os.path.join(monotaro_dir, 'best_model_v2.pt'))
        else:
            patience_counter += 1
            if patience_counter >= PATIENCE:
                print(f">>> Early stopping at epoch {epoch+1}")
                break
    
    # Final Evaluation
    print(">>> [4/5] Final Evaluation...")
    model.load_state_dict(torch.load(os.path.join(monotaro_dir, 'best_model_v2.pt')))
    model.eval()
    
    all_preds, all_trues = [], []
    with torch.no_grad():
        for batch in valid_loader:
            inp, mask, top, lbl = [b.to(DEVICE) for b in batch]
            logits = model(inp, mask, top)
            preds = torch.argmax(logits, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_trues.extend(lbl.cpu().numpy())
    
    acc = accuracy_score(all_trues, all_preds) * 100
    p, r, f1, _ = precision_recall_fscore_support(all_trues, all_preds, average='macro', zero_division=0)
    
    print("\n" + "=" * 60)
    print(" MonotaRO RESULTS (High-Accuracy Pipeline v2)")
    print("=" * 60)
    print(f" Model: {MODEL_NAME}")
    print(f" Data Augmentation: {USE_DATA_AUGMENTATION}")
    print(f" Loss: Focal Loss (gamma=2.0)")
    print("-" * 60)
    print(f" Classification: 3-class (不満/普通/満足)")
    print(f" Train: {len(train_data)} | Valid: {len(valid_data)}")
    print("-" * 60)
    print(f" Accuracy : {acc:.2f}%")
    print(f" Precision: {p*100:.2f}%")
    print(f" Recall   : {r*100:.2f}%")
    print(f" F1-Score : {f1*100:.2f}%")
    print("-" * 60)
    print(" Per-Class Report:")
    print(classification_report(all_trues, all_preds, target_names=['不満', '普通', '満足'], zero_division=0))
    print("=" * 60)
    print(f" Best Accuracy: {best_acc:.2f}%")
    print(f" Best F1: {best_f1*100:.2f}%")
    print("=" * 60)
