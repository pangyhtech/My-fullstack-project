# -*- coding: utf-8 -*-
"""
MonotaRO Q&A System - Model-based Inference Module
訓練データを使用した満足度予測
"""

import os
import sys
import random
import json

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if os.path.join(parent_dir, "reproduce") not in sys.path:
    sys.path.insert(0, os.path.join(parent_dir, "reproduce"))
if os.path.join(parent_dir, "KG_tail_prediction") not in sys.path:
    sys.path.insert(0, os.path.join(parent_dir, "KG_tail_prediction"))

try:
    from TuckER_model import TuckER
    KG_AVAILABLE = True
except ImportError:
    KG_AVAILABLE = False
    print("[Warning] TuckER model not available")


# Load real product data from training
PRODUCT_DATA_PATH = os.path.join(current_dir, "product_data.json")
REAL_PRODUCT_DATA = {}
try:
    with open(PRODUCT_DATA_PATH, 'r', encoding='utf-8') as f:
        REAL_PRODUCT_DATA = json.load(f)
    print(f"[Inference] Loaded real product data: {len(REAL_PRODUCT_DATA)} categories")
except Exception as e:
    print(f"[Inference] Could not load product data: {e}")

# Optional imports
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("[Warning] PyTorch not available")

try:
    from transformers import AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("[Warning] Transformers not available")

# ==========================================
# カテゴリ定義 (24カテゴリ)
# ==========================================
# ==========================================
# カテゴリ定義 (JSONから動的ロード)
# ==========================================
CATEGORY_LIST = sorted(list(REAL_PRODUCT_DATA.keys()))

# 各カテゴリの代表商品 (JSONから動的ロード)
CATEGORY_PRODUCTS = {}
for i, cat in enumerate(CATEGORY_LIST):
    CATEGORY_PRODUCTS[i] = sorted(list(REAL_PRODUCT_DATA[cat].keys()))



# カテゴリの価格帯
CATEGORY_PRICES = {
    0: (1980, 4980), 1: (498, 2980), 2: (1280, 5980), 3: (198, 980),
    4: (9800, 39800), 5: (1480, 8980), 6: (980, 7980), 7: (4980, 34800),
    8: (498, 2480), 9: (580, 4980), 10: (298, 1980), 11: (1980, 14800),
    12: (498, 3980), 13: (298, 2480), 14: (98, 798), 15: (980, 7980),
    16: (1480, 9800), 17: (980, 5980), 18: (498, 3480), 19: (2980, 19800),
    20: (1480, 9800), 21: (298, 1980), 22: (498, 3980), 23: (498, 3980),
}

# 満足度ラベル
SATISFACTION_LABELS = {
    0: {"label": "不満", "emoji": "😞", "class": "negative"},
    1: {"label": "普通", "emoji": "😐", "class": "neutral"},
    2: {"label": "満足", "emoji": "😊", "class": "positive"},
}

# ==========================================
# XLM-RoBERTa モデル定義
# ==========================================
if TORCH_AVAILABLE:
    class HighAccuracyClassifierV2(nn.Module):
        """XLM-RoBERTa ベースの満足度分類器"""
        
        def __init__(self, backbone, hidden_size=768, topic_num=24, num_classes=3):
            super().__init__()
            self.backbone = backbone
            self.hidden_size = hidden_size
            self.topic_embed = nn.Embedding(topic_num, 128)
            
            self.classifier = nn.Sequential(
                nn.Linear(hidden_size + 128, 512),
                nn.LayerNorm(512),
                nn.GELU(),
                nn.Dropout(0.3),
                nn.Linear(512, 256),
                nn.LayerNorm(256),
                nn.GELU(),
                nn.Dropout(0.2),
                nn.Linear(256, num_classes)
            )
        
        def forward(self, input_ids, attention_mask, topics):
            outputs = self.backbone(input_ids, attention_mask=attention_mask)
            
            if hasattr(outputs, 'last_hidden_state'):
                cls_output = outputs.last_hidden_state[:, 0, :]
            else:
                cls_output = outputs[0][:, 0, :]
            
            topic_emb = self.topic_embed(topics)
            combined = torch.cat([cls_output, topic_emb], dim=-1)
            
            logits = self.classifier(combined)
            return logits


# ==========================================
# 応答テンプレート（尊敬語対応）
# ==========================================
RESPONSE_TEMPLATES = {
    "price": [
        "こちらの{product}は税込み{price}円でございます。",
        "{product}のお値段は{price}円（税込）となっております。ご検討いただけますと幸いです。",
        "お問い合わせありがとうございます。{price}円でご提供しております。",
    ],
    "stock": [
        "はい、{product}は在庫がございます。すぐにお届け可能でございます。",
        "こちらの商品は在庫十分にございます。ご安心ください。",
        "申し訳ございません。現在在庫を確認中でございます。",
    ],
    "delivery": [
        "通常2〜3営業日以内にお届けいたします。",
        "最短で翌日お届けが可能でございます。（地域によります）",
        "ご注文確定後、3日以内に発送させていただきます。",
    ],
    "spec": [
        "{product}の詳細仕様についてご案内いたします。ご不明点がございましたらお申し付けください。",
        "サイズや仕様については商品ページにて確認いただけます。",
        "各種サイズを取り揃えております。ご希望をお知らせください。",
    ],
    "recommend": [
        "{category}カテゴリでは、{product}が大変人気でございます。",
        "お客様のご用途に合わせて最適な商品をご提案いたします。",
        "初めてのお客様には{product}がおすすめでございます。",
    ],
    "return": [
        "返品・交換につきましては、商品到着後7日以内にご連絡をお願いいたします。",
        "未開封・未使用の場合、返品を承っております。",
        "万が一の不良品につきましては、無償で交換させていただきます。",
    ],
    "quality": [
        "こちらの商品は厳格な品質管理のもと製造されております。",
        "JIS規格に準拠した高品質な商品でございます。",
        "多くのお客様からご好評をいただいております。",
    ],
    "greeting": [
        "いらっしゃいませ。MonotaRO カスタマーサポートでございます。本日はどのようなご用件でしょうか？",
        "お問い合わせありがとうございます。何かお手伝いできることはございますか？",
        "ご来店ありがとうございます。{category}カテゴリの商品をご案内いたします。",
    ],
    "thanks": [
        "こちらこそありがとうございます。またのご利用を心よりお待ちしております。",
        "ご利用いただきありがとうございます。他にご質問がございましたらお気軽にどうぞ。",
        "お役に立てて光栄でございます。今後ともMonotaROをよろしくお願いいたします。",
    ],
    "complaint": [
        "ご不便をおかけして大変申し訳ございません。早急に対応させていただきます。",
        "ご迷惑をおかけし、誠に申し訳ございません。詳細をお聞かせいただけますでしょうか。",
        "貴重なご意見をいただきありがとうございます。改善に努めてまいります。",
    ],
    "fallback": [
        "かしこまりました。ご質問について確認させていただきます。",
        "ご質問ありがとうございます。もう少し詳しくお聞かせいただけますでしょうか。",
        "承知いたしました。担当者より折り返しご連絡させていただきます。",
    ],
}

# 尊敬語・丁寧語検出キーワード
POLITE_KEYWORDS = [
    "ございます", "いただ", "くださ", "おります", "存じ", "申し",
    "伺い", "お願い", "承知", "かしこまり", "恐れ入り",
]

# ネガティブ感情キーワード（より包括的）
# ネガティブ感情キーワード（より包括的）
# 注意: 単なる問い合わせ（返品方法など）はネガティブに含まないように除外
NEGATIVE_KEYWORDS = [
    # 直接的なクレーム
    "クレーム", "苦情", "トラブル",
    # 品質への不満（"問題"は質問でも使うので除外、文脈依存）
    "壊れ", "不良", "故障", "破損", "汚れ", "傷", "動かない",
    # サービスへの不満
    "遅い", "届かない", "届いてない", "間違", "違う", "来ない",
    # 感情表現
    "怒", "腹立", "ひどい", "最悪", "最低", "がっかり", "失望", "残念", "ふざけ",
    # 強い拒絶
    "二度と", "金返せ", "詐欺",
    # 敬語での不満表現
    "いただけません", "困って", "納得できません", "承服しかねます",
]

# 丁寧語・クッション言葉（これらが含まれていてもネガティブと判定しない）
# ユーザー指摘対応: 「すみません、質問ですが」などは普通（Neutral）とすべき
POLITE_IGNORE_KEYWORDS = [
    "すみません", "すいません", "恐れ入ります", "失礼します", "ごめん", 
    "お忙しいところ", "質問", "聞きたい", "教えて",
]

# 客観的な問い合わせキーワード（これらのみの場合は「普通」と判定する）
OBJECTIVE_KEYWORDS = [
    # 価格・見積
    "価格", "値段", "いくら", "見積", "金額", "費用",
    # 在庫・納期
    "在庫", "ある？", "ない？", "納期", "いつ", "日", "発送", "配送", "届く",
    # 商品仕様
    "サイズ", "寸法", "重さ", "重量", "スペック", "仕様", "材質", "素材", "使える", "用途",
    "取り付け", "設置", "使い方", "方法", "どう", "難し", "耐荷重",
    # ユーザー指摘対応：技術仕様・ポイント
    "回転数", "rpm", "トルク", "電圧", "電流", "ポイント", "還元", "キャンペーン", 
    "商品", "について",
    # 手続き・書類
    "領収書", "請求書", "インボイス", "宛名", "返品", "交換", "キャンセル", "注文", "変更", "変え",
]

# ポジティブ感情キーワード
POSITIVE_KEYWORDS = [
    # 感謝
    "ありがとう", "感謝", "助かり", "おかげ",
    # 満足
    "満足", "嬉しい", "喜", "良い", "いい", "素晴らしい", "最高", "完璧",
    # 推薦
    "おすすめ", "気に入", "リピート", "また買",
    # 品質評価
    "しっかり", "丈夫", "きれい", "綺麗",
    # 敬語でのポジティブ表現
    "助かりました", "ありがとうございました", "感謝申し上げ",
]


class MonotaROInference:
    """MonotaRO Q&A 推論エンジン（モデルベース）"""
    
    def __init__(self, model_path=None):
        """初期化"""
        self.device = 'cpu'
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.current_category = None
        self.current_product = None
        self.current_price = None  # 訓練データからの実価格
        self.dialogue_history = []
        
        # KG Model
        self.kg_model = None
        self.kg_e2id = {}
        self.kg_r2id = {}
        self.kg_id2e = {}
        self.kg_loaded = False
        
        # デフォルトのモデルパス

        if model_path is None:
            model_path = os.path.join(parent_dir, "best_model_v2.pt")
        
        print(f"[Inference] Initializing...")
        
        if TORCH_AVAILABLE and TRANSFORMERS_AVAILABLE:
            self._load_model(model_path)
        else:
            print("[Inference] Using rule-based inference (PyTorch/Transformers not available)")
            
        if KG_AVAILABLE and TORCH_AVAILABLE:
            self._load_kg_model()

    
    def _load_model(self, model_path):
        """モデルをロード (run_full_pipeline.pyと同じ構成)"""
        try:
            # GPU利用可能かチェック
            if torch.cuda.is_available():
                self.device = 'cuda'
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                self.device = 'mps'
            print(f"[Inference] Using device: {self.device}")
            
            backbone = None
            hidden_size = 768
            
            # 1. Try XLM-RoBERTa (Primary)
            try:
                print("[Inference] Trying to load XLM-RoBERTa...")
                self.tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
                backbone = AutoModel.from_pretrained("xlm-roberta-base")
                hidden_size = backbone.config.hidden_size
                print("[Inference] Loaded XLM-RoBERTa")
            except Exception as e:
                print(f"[Inference] XLM-RoBERTa failed: {e}")
                
                # 2. Try BERT Japanese (Secondary)
                try:
                    print("[Inference] Trying to load cl-tohoku/bert-base-japanese-v2...")
                    self.tokenizer = AutoTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-v2")
                    backbone = AutoModel.from_pretrained("cl-tohoku/bert-base-japanese-v2")
                    hidden_size = backbone.config.hidden_size
                    print("[Inference] Loaded cl-tohoku/bert-base-japanese-v2")
                except Exception as e2:
                    print(f"[Inference] BERT-Japanese failed: {e2}")
                    
                    # 3. Fallback to Multilingual BERT
                    print("[Inference] Falling back to Multilingual BERT...")
                    self.tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
                    backbone = AutoModel.from_pretrained("bert-base-multilingual-cased")
                    hidden_size = 768

            # 学習時と同じ特殊トークン
            self.tokenizer.add_special_tokens({'additional_special_tokens': ['[NO_TOKEN]']})
            backbone.resize_token_embeddings(len(self.tokenizer))
            
            # モデルを構築
            self.model = HighAccuracyClassifierV2(
                backbone=backbone, 
                hidden_size=hidden_size, 
                topic_num=24, 
                num_classes=3
            ).to(self.device)
            
            # 学習済み重みをロード
            if os.path.exists(model_path):
                print(f"[Inference] Loading weights from {model_path}")
                state_dict = torch.load(model_path, map_location=self.device, weights_only=True)
                # strict=Falseで互換性のある重みのみロード
                incompatible = self.model.load_state_dict(state_dict, strict=False)
                if incompatible.missing_keys:
                    print(f"[Inference] Missing keys: {len(incompatible.missing_keys)}")
                if incompatible.unexpected_keys:
                    print(f"[Inference] Unexpected keys: {len(incompatible.unexpected_keys)}")
                self.model_loaded = True
                print("[Inference] Model loaded successfully!")
            else:
                print(f"[Inference] Model file not found: {model_path}")
                print("[Inference] Using randomly initialized weights")
            
            self.model.eval()
            
        except Exception as e:
            print(f"[Inference] Error loading model: {e}")
            import traceback
            traceback.print_exc()
            self.model_loaded = False
            
    def _load_kg_model(self):
        """知識グラフモデル (TuckER) をロード"""
        try:
            import pickle
            kg_dir = os.path.join(parent_dir, 'KG_tail_prediction')
            mapping_path = os.path.join(kg_dir, 'data/kg_mappings.pkl')
            model_path = os.path.join(kg_dir, 'model/TuckER_model_trained.pkl')
            
            if os.path.exists(mapping_path) and os.path.exists(model_path):
                print(f"[Inference] Loading KG mappings from {mapping_path}")
                with open(mapping_path, 'rb') as f:
                    mappings = pickle.load(f)
                    self.kg_e2id = mappings['entity2id']
                    self.kg_r2id = mappings['relation2id']
                    self.kg_id2e = mappings['id2entity']
                
                print(f"[Inference] Loading KG model from {model_path}")
                # Use same dims as training script
                self.kg_model = TuckER(
                    len(self.kg_e2id),
                    len(self.kg_r2id),
                    d1=200, d2=200, # Default per train_tucker_kg.py
                    input_dropout=0.3, hidden_dropout1=0.4, hidden_dropout2=0.5
                ).to('cpu') # Inference on CPU is fine
                
                self.kg_model.load_state_dict(torch.load(model_path, map_location='cpu'))
                self.kg_model.eval()
                self.kg_loaded = True
                print("[Inference] KG Model loaded successfully!")
            else:
                print("[Inference] KG model/mapping not found. Run reproduce/train_tucker_kg.py first.")
        except Exception as e:
            print(f"[Inference] Error loading KG model: {e}")
            import traceback
            traceback.print_exc()

    def predict_kg_tail(self, head_entity: str, relation: str) -> list:
        """知識グラフで推論 (Head, Relation, ?) -> Top 3 Tails"""
        if not self.kg_loaded:
            return []
            
        # 安全策: 部分一致でエンティティを探す
        h_id = self.kg_e2id.get(head_entity)
        if h_id is None:
            # 簡易サーチ
            for name, eid in self.kg_e2id.items():
                if head_entity in name or name in head_entity:
                    h_id = eid
                    break
        
        r_id = self.kg_r2id.get(relation)
        
        if h_id is not None and r_id is not None:
            try:
                with torch.no_grad():
                    h_tensor = torch.tensor([h_id])
                    r_tensor = torch.tensor([r_id])
                    
                    pred = self.kg_model.forward(h_tensor, r_tensor)
                    # Get top 3
                    scores, indices = torch.topk(pred, 3)
                    
                    results = []
                    for idx in indices[0]:
                        ent_name = self.kg_id2e.get(idx.item(), "Unknown")
                        results.append(ent_name)
                    return results
            except Exception as e:
                print(f"[Inference] KG Predict Error: {e}")
        
        return []

    def set_category(self, category_idx: int) -> dict:

        """カテゴリを設定"""
        if 0 <= category_idx < len(CATEGORY_LIST):
            self.current_category = category_idx
            self.current_product = None
            self.dialogue_history = []
            
            products = CATEGORY_PRODUCTS.get(category_idx, [])
            return {
                "success": True,
                "category_name": CATEGORY_LIST[category_idx],
                "category_id": category_idx,
                "products": products,
                "message": f"「{CATEGORY_LIST[category_idx]}」カテゴリが選択されました。商品をお選びください。"
            }
        return {"success": False, "error": "無効なカテゴリです"}
    
    def set_product(self, product_name: str) -> dict:
        """商品を設定（訓練データの詳細情報を使用）"""
        if self.current_category is None:
            return {"success": False, "error": "先にカテゴリを選択してください"}
        
        category_name = CATEGORY_LIST[self.current_category]
        products = CATEGORY_PRODUCTS.get(self.current_category, [])
        
        # 訓練データにある商品も含める
        real_products = list(REAL_PRODUCT_DATA.get(category_name, {}).keys())
        all_products = list(set(products + real_products))
        
        if product_name in all_products:
            self.current_product = product_name
            self.dialogue_history = []
            
            # 訓練データから情報を取得
            product_info = REAL_PRODUCT_DATA.get(category_name, {}).get(product_name, {})
            self.current_params = product_info.get("params", {})
            self.current_qa_list = product_info.get("qa", [])
            
            # 価格設定
            price_str = self.current_params.get("price", "9,800円")
            # "9,800円" -> 9800
            try:
                self.current_price = int(price_str.replace(",", "").replace("円", ""))
            except:
                self.current_price = 9800
            
            return {
                "success": True,
                "product": product_name,
                "price": self.current_price,
                "category": category_name,
                "message": f"「{product_name}」が選択されました。ご質問をどうぞ。"
            }
        return {"success": False, "error": f"「{product_name}」は選択できません"}

    def _find_best_match_qa(self, query: str) -> str:
        """訓練データから最も類似した質問への回答を検索"""
        if not self.current_qa_list:
            return None
            
        best_ratio = 0.0
        best_answer = None
        
        from difflib import SequenceMatcher
        
        for qa in self.current_qa_list:
            q_text = qa["q"]
            # 単純な類似度計算
            ratio = SequenceMatcher(None, query, q_text).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_answer = qa["a"]
        
        # 閾値を設定（あまりに低い場合はマッチしないとする）
        if best_ratio > 0.6:
            return best_answer
        return None

    def predict_satisfaction(self, text: str) -> int:
        """ルール + モデルを使用して満足度を予測"""
        
        # まず、明確なキーワードをルールベースでチェック（最優先）
        rule_result = self._check_obvious_sentiment(text)
        if rule_result is not None:
            return rule_result
        
        # モデルが利用可能な場合は、モデルで予測
        if self.model is not None and self.tokenizer is not None:
            try:
                full_text = " ||| ".join(self.dialogue_history[-5:] + [text])
                
                encoded = self.tokenizer(
                    full_text,
                    max_length=256,
                    truncation=True,
                    padding='max_length',
                    return_tensors='pt'
                )
                
                input_ids = encoded['input_ids'].to(self.device)
                attention_mask = encoded['attention_mask'].to(self.device)
                topic = torch.tensor([self.current_category or 0]).to(self.device)
                
                with torch.no_grad():
                    logits = self.model(input_ids, attention_mask, topic)
                    probs = torch.softmax(logits, dim=1)
                    prediction = torch.argmax(logits, dim=1).item()
                    confidence = probs[0, prediction].item()
                
                # --- Safety Net for Model Prediction ---
                # モデルが「不満(0)」と予測しても、客観的な質問キーワードやクッション言葉が含まれ、かつ強いネガティブ語がない場合は「普通(1)」に補正
                if prediction == 0:
                    is_objective = any(k in text for k in OBJECTIVE_KEYWORDS)
                    is_polite = any(k in text for k in POLITE_IGNORE_KEYWORDS)
                    has_strong_negative = any(k in text for k in NEGATIVE_KEYWORDS)
                    
                    if (is_objective or is_polite) and not has_strong_negative:
                        print(f"[Inference] Override model prediction 0 -> 1 (Objective/Polite: {text})")
                        return 1

                # 信頼度が低い場合はルールベースにフォールバック
                if confidence < 0.5:
                    return self._predict_satisfaction_rule_based(text)
                
                return prediction
                
            except Exception as e:
                print(f"[Inference] Model prediction error: {e}")
        
        # フォールバック: ルールベース
        return self._predict_satisfaction_rule_based(text)
    
    def _check_obvious_sentiment(self, text: str) -> int:
        """明確な感情表現をチェック（最優先）"""
        
        # 強いネガティブ表現 (誤検知を防ぐため、明らかに感情的なものに限定)
        strong_negative = [
            "最悪", "ひどい", 
            "クレーム", "怒", "腹立", "失望", "残念", "ふざけ", "二度と", "金返せ", "詐欺",
            "対応が悪い", "態度が悪い"
        ]
        # 文脈依存の単語 ("返品"など) はリストから除外
        
        for keyword in strong_negative:
            if keyword in text:
                return 0  # 不満
        
        # 客観的な質問の場合、ここで「普通」と確定させる (Safety Net 1)
        # これにより、モデルや他のルールが誤って不満と判定するのを防ぐ
        is_objective = any(k in text for k in OBJECTIVE_KEYWORDS)
        is_polite = any(k in text for k in POLITE_IGNORE_KEYWORDS)
        has_negative_context = any(k in text for k in NEGATIVE_KEYWORDS)
        
        if (is_objective or is_polite) and not has_negative_context:
             return 1 # 普通
        
        # 強いポジティブ表現
        strong_positive = [
            "ありがとう", "感謝", "助かり", "嬉しい", "満足", "最高",
            "素晴らしい", "完璧", "おすすめ", "気に入", "良かった", "いい感じ"
        ]
        for keyword in strong_positive:
            if keyword in text:
                return 2  # 満足
        
        return None  # 明確な判断ができない場合
    
    def _predict_satisfaction_rule_based(self, text: str) -> int:
        """ルールベースの満足度予測（フォールバック）"""
        # ネガティブチェック
        for keyword in NEGATIVE_KEYWORDS:
            if keyword in text:
                return 0
        
        # ポジティブチェック
        for keyword in POSITIVE_KEYWORDS:
            if keyword in text:
                return 2
        
        # デフォルトは普通
        return 1
    
    def detect_intent(self, text: str) -> str:
        """インテントを検出"""
        text_lower = text.lower()
        
        # 挨拶
        if any(w in text for w in ["こんにちは", "おはよう", "こんばんは", "はじめまして", "よろしく"]):
            return "greeting"
        
        # 感謝
        if any(w in text for w in ["ありがとう", "サンキュー", "感謝", "助かり"]):
            return "thanks"
        
        # クレーム
        if any(w in text for w in NEGATIVE_KEYWORDS[:10]):
            return "complaint"
        
        # 価格
        if any(w in text for w in ["いくら", "値段", "価格", "円", "お金", "コスト", "なんぼ", "おいくら"]):
            return "price"
        
        # 在庫
        if any(w in text for w in ["在庫", "ある", "ありますか", "入荷", "品切れ", "売り切れ", "ございますか"]):
            return "stock"
        
        # 配送
        if any(w in text for w in ["届く", "届き", "配送", "納期", "発送", "いつ届く", "配達", "何日"]):
            return "delivery"
        
        # スペック
        if any(w in text for w in ["サイズ", "寸法", "重さ", "重量", "スペック", "仕様", "大きさ"]):
            return "spec"
        
        # おすすめ
        if any(w in text for w in ["おすすめ", "オススメ", "選び方", "どれがいい", "比較", "人気"]):
            return "recommend"
        
        # 返品
        if any(w in text for w in ["返品", "交換", "キャンセル", "返金"]):
            return "return"
        
        # 品質
        if any(w in text for w in ["品質", "丈夫", "長持ち", "耐久", "保証"]):
            return "quality"
        
        return "fallback"

    def generate_response(self, message: str) -> dict:
        """応答を生成（RAG + ルール + モデル）"""
        # 対話履歴に追加
        self.dialogue_history.append(f"Q: {message}")
        
        # 意図検出 (共通で使用)
        detected_intent = self.detect_intent(message)
        
        # 1. 訓練データからの検索 (Retrieval)
        retrieved_answer = self._find_best_match_qa(message)
        
        # 2. パラメータ検索 (Spec retrieval)
        extracted_param_ans = None
        if not retrieved_answer:
            # 簡易的なパラメータ抽出
            if "価格" in message or "いくら" in message:
                if "price" in self.current_params:
                    extracted_param_ans = f"価格は{self.current_params['price']}です。"
            elif "重さ" in message or "重量" in message:
                 if "weight" in self.current_params:
                    extracted_param_ans = f"重量は{self.current_params['weight']}です。"
            elif "サイズ" in message or "寸法" in message or "大きさ" in message:
                 if "size" in self.current_params:
                    extracted_param_ans = f"サイズは{self.current_params['size']}です。"
            
            if extracted_param_ans:
                retrieved_answer = extracted_param_ans

        # 満足度予測 (共通処理)
        if self.model_loaded:
            satisfaction = self.predict_satisfaction(message)
        else:
            satisfaction = self._predict_satisfaction_rule_based(message)

        # 3. 知識グラフ推論 (Reasoning)
        kg_insight = None
        if self.kg_loaded and self.current_product:
            # インテントから関係性をマッピング
            rel_map = {
                "price": "属性", # "価格"関係がないので属性として推論
                "spec": "属性",
                "quality": "属性",
                "recommend": "カテゴリ"
            }
            target_rel = rel_map.get(detected_intent, "属性")
            
            kg_preds = self.predict_kg_tail(self.current_product, target_rel)
            if kg_preds:
                kg_insight = f"【AI推論】知識グラフによると、{self.current_product}は「{', '.join(kg_preds)}」と関連があります。"

        # 応答の決定
        if retrieved_answer:
            response = retrieved_answer
            intent = "retrieval"
        else:
            # フォールバック: 既存のロジック
            intent = detected_intent
            
            # 応答テンプレートを選択
            templates = RESPONSE_TEMPLATES.get(intent, RESPONSE_TEMPLATES["fallback"])
            response_template = random.choice(templates)
            
            # テンプレート変数を置換
            product = self.current_product or "商品"
            category = CATEGORY_LIST[self.current_category] if self.current_category is not None else "商品"
            price = self.current_price or 9802

            
            response = response_template.format(
                product=product,
                category=category,
                price=f"{price:,}"
            )

        
        # KG推論結果を付与
        if kg_insight:
            response += f"\n\n{kg_insight}"
        
        sat_info = SATISFACTION_LABELS[satisfaction]

        
        # 対話履歴に追加
        self.dialogue_history.append(f"A: {response}")
        
        return {
            "response": response,
            "satisfaction": satisfaction,
            "satisfaction_label": f"{sat_info['label']} {sat_info['emoji']}",
            "satisfaction_class": sat_info['class'],
            "category": CATEGORY_LIST[self.current_category] if self.current_category is not None else "Unknown",
            "product": self.current_product or "Unknown",
            "intent": intent,
            "model_based": self.model_loaded,
        }
    
    def get_categories(self) -> list:
        """カテゴリ一覧を取得"""
        return [{"id": i, "name": cat} for i, cat in enumerate(CATEGORY_LIST)]
    
    def get_products(self, category_id: int) -> list:
        """指定カテゴリの商品一覧を取得"""
        return CATEGORY_PRODUCTS.get(category_id, [])
    
    def reset_dialogue(self):
        """対話をリセット"""
        self.dialogue_history = []
        return {"success": True, "message": "対話履歴がリセットされました"}


# グローバルインスタンス
_inference_engine = None


def get_inference_engine():
    """シングルトンパターンでインスタンスを取得"""
    global _inference_engine
    if _inference_engine is None:
        _inference_engine = MonotaROInference()
    return _inference_engine




def generate_response(message: str) -> dict:
    """便利関数"""
    engine = get_inference_engine()
    return engine.generate_response(message)


# テスト
if __name__ == "__main__":
    engine = MonotaROInference()
    
    print("\n" + "=" * 60)
    print(" MonotaRO Q&A Inference Test (Model-Based)")
    print("=" * 60)
    
    # カテゴリ選択 (ヘルメットを探す)
    target_product = "ヘルメット"
    target_cat_id = -1
    
    for i, cat in enumerate(CATEGORY_LIST):
        products = engine.get_products(i)
        if target_product in products:
            target_cat_id = i
            break
    
    if target_cat_id != -1:
        result = engine.set_category(target_cat_id)
        print(f"\n>>> {result.get('message', 'カテゴリ選択失敗')}")
        
        # 商品選択
        result = engine.set_product(target_product)
        print(f"\n>>> {result.get('message', result.get('error'))}")
    else:
        print(f"Product {target_product} not found in any category.")
        # Fallback to category 0
        engine.set_category(0)
        engine.set_product(engine.get_products(0)[0])

    
    # テストメッセージ
    test_messages = [
        "このヘルメットはいくらですか？",
        "在庫はございますか？",
        "いつ届きますか？",
        "耐荷重はどれくらいですか？",
        "すみません、棚について質問なんですが。", # User reported: Polite start -> should be Neutral
        "最大回転数は？", # User reported: Technical spec -> sould be Neutral
        "お忙しいところすみません", # User reported: Polite apology -> should be Neutral
        "ポイント何倍？", # User reported: Points inquiry -> should be Neutral
        "商品が壊れていました。返品したいです。",
        "とても助かりました。ありがとうございます！",
    ]
    
    for msg in test_messages:
        result = engine.generate_response(msg)
        print(f"\n[Q] {msg}")
        print(f"[A] {result['response']}")
        print(f"    満足度: {result['satisfaction_label']}")
        print(f"    モデル推論: {result['model_based']}")
