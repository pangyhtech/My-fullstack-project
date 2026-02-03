# -*- coding: utf-8 -*-
"""
MonotaRO TuckER 知識グラフ訓練スクリプト

このスクリプトは真実の知識グラフデータを使用してTuckERモデルを訓練します。

=== 真実KGデータの作り方 ===

1. 三元組データ形式:
   (Head, Relation, Tail) の形式で用意
   
   例:
   ヘルメット, 属性, 安全規格
   ヘルメット, カテゴリ, 安全保護具
   ドリルビット, 材質, 超硬合金
   ドリルビット, 用途, 金属加工

2. データソース (MonotaRO向け):
   - MonotaRO商品ページの仕様表をスクレイピング
   - JIS規格データベースから属性抽出
   - Amazon/楽天の類似商品情報

3. ファイル形式:
   monotaro/KG_tail_prediction/data/kg_triples.txt
   
   内容例:
   ヘルメット\t属性\t耐衝撃性
   ヘルメット\t規格\tJIS_T8131
   安全靴\t属性\t滑り止め
   ...
"""

import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from tqdm import tqdm

# パス設定
current_dir = os.path.dirname(os.path.abspath(__file__))
monotaro_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.join(monotaro_dir, 'KG_tail_prediction'))

from TuckER_model import TuckER

# ==========================================
# Config
# ==========================================
EMBEDDING_DIM = 200
EPOCHS = 100
BATCH_SIZE = 128
LR = 0.003
DEVICE = 'cpu'

# ==========================================
# Data Loading
# ==========================================
def load_kg_triples(filepath):
    """三元組データを読み込み"""
    triples = []
    entities = set()
    relations = set()
    
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Generating sample triples...")
        return generate_sample_triples()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                h, r, t = parts
                triples.append((h, r, t))
                entities.add(h)
                entities.add(t)
                relations.add(r)
    
    return triples, list(entities), list(relations)

def generate_sample_triples():
    """サンプル三元組データを生成 (デモ用)"""
    # 商品と属性の関係を定義
    triples = []
    
    products = {
        'ヘルメット': ['耐衝撃性', 'JIS規格', '通気性', '軽量'],
        '安全靴': ['滑り止め', '耐油性', '鉄芯入り', '静電気防止'],
        'ドリルビット': ['超硬合金', '高速回転', 'ステンレス対応', '長寿命'],
        '安全帯': ['フルハーネス', '墜落防止', '規格適合', '軽量'],
        'ノギス': ['高精度', 'ステンレス製', 'デジタル表示', '防水'],
    }
    
    relations = ['属性', 'カテゴリ', '材質', '規格', '用途']
    
    for product, attrs in products.items():
        for attr in attrs:
            triples.append((product, '属性', attr))
        triples.append((product, 'カテゴリ', '工業用品'))
    
    entities = set()
    rels = set()
    for h, r, t in triples:
        entities.add(h)
        entities.add(t)
        rels.add(r)
    
    return triples, list(entities), list(rels)

# ==========================================
# Training
# ==========================================
def train_tucker(triples, entities, relations, epochs=EPOCHS):
    """TuckERモデルを訓練"""
    
    # ID マッピング
    entity2id = {e: i for i, e in enumerate(entities)}
    relation2id = {r: i for i, r in enumerate(relations)}
    
    num_entities = len(entities)
    num_relations = len(relations)
    
    print(f">>> Entities: {num_entities}, Relations: {num_relations}, Triples: {len(triples)}")
    
    # モデル初期化 (正しい引数順序: ent_len, rel_len, d1, d2, **kwargs)
    model = TuckER(
        num_entities, 
        num_relations, 
        EMBEDDING_DIM, 
        EMBEDDING_DIM,
        input_dropout=0.3,
        hidden_dropout1=0.4,
        hidden_dropout2=0.5
    ).to(DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=LR)
    
    # データ準備
    triple_ids = [(entity2id[h], relation2id[r], entity2id[t]) for h, r, t in triples]
    
    print(f">>> Training TuckER for {epochs} epochs...")
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        np.random.shuffle(triple_ids)
        
        for i in range(0, len(triple_ids), BATCH_SIZE):
            batch = triple_ids[i:i+BATCH_SIZE]
            
            heads = torch.tensor([t[0] for t in batch]).to(DEVICE)
            rels = torch.tensor([t[1] for t in batch]).to(DEVICE)
            tails = torch.tensor([t[2] for t in batch]).to(DEVICE)
            
            optimizer.zero_grad()
            
            # Forward
            predictions = model.forward(heads, rels)
            
            # Binary Cross Entropy Loss
            labels = torch.zeros(len(batch), num_entities).to(DEVICE)
            for j, t in enumerate(tails):
                labels[j, t] = 1
            
            loss = nn.BCEWithLogitsLoss()(predictions, labels)
            
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        if (epoch + 1) % 10 == 0:
            print(f"    Epoch {epoch+1}/{epochs}: Loss = {total_loss:.4f}")
    
    # 保存
    save_path = os.path.join(monotaro_dir, 'KG_tail_prediction/model/TuckER_model_trained.pkl')
    torch.save(model.state_dict(), save_path)
    print(f">>> Model saved to {save_path}")
    
    # マッピング保存
    import pickle
    mapping_path = os.path.join(monotaro_dir, 'KG_tail_prediction/data/kg_mappings.pkl')
    with open(mapping_path, 'wb') as f:
        pickle.dump({'entity2id': entity2id, 'relation2id': relation2id, 
                     'id2entity': {v:k for k,v in entity2id.items()},
                     'id2relation': {v:k for k,v in relation2id.items()}}, f)
    print(f">>> Mappings saved to {mapping_path}")
    
    return model, entity2id, relation2id

# ==========================================
# Main
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print(" MonotaRO TuckER Knowledge Graph Training")
    print("=" * 60)
    
    # 三元組データ読み込み
    kg_file = os.path.join(monotaro_dir, 'KG_tail_prediction/data/kg_triples.txt')
    triples, entities, relations = load_kg_triples(kg_file)
    
    if not triples:
        triples, entities, relations = generate_sample_triples()
    
    # 訓練
    model, e2id, r2id = train_tucker(triples, entities, relations)
    
    print("\n" + "=" * 60)
    print(" Training Complete!")
    print("=" * 60)
    print(f" Entities: {len(e2id)}")
    print(f" Relations: {len(r2id)}")
    print(" 次のステップ:")
    print("   1. monotaro/KG_tail_prediction/data/kg_triples.txt に実データを追加")
    print("   2. このスクリプトを再実行して本番モデルを訓練")
    print("=" * 60)
