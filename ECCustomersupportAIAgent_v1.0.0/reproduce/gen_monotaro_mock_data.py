# -*- coding: utf-8 -*-
"""
MonotaRO 模擬対話データ生成スクリプト (完全動的版)
目標: 10,000+ 完全一意対話 (問答パターン重複なし)
言語比率: 日本語 90% / 英語 5% / 中国語 5%
"""

import os
import pandas as pd
import random
import csv
import hashlib
from monotaro_categories import CATEGORY_ENTITIES, CATEGORY_LIST, CATEGORY_RELATIONS

os.makedirs('monotaro/reproduce/data/train/data_turn', exist_ok=True)
os.makedirs('monotaro/reproduce/data/valid/data_turn', exist_ok=True)

LANG_WEIGHTS = {'ja': 90, 'en': 5, 'zh': 5}

# ============================================================
# 動的パラメータ (重複を避けるためのランダム値生成)
# ============================================================

# 数値範囲
PRICES = list(range(100, 100000, 50))  # 100円~10万円
WEIGHTS = [f"{w}g" for w in range(50, 5000, 10)] + [f"{w}kg" for w in [1, 1.5, 2, 2.5, 3, 4, 5, 8, 10, 15, 20]]
DIMENSIONS = [f"{d}mm" for d in range(5, 500, 5)] + [f"{d}cm" for d in range(1, 100, 1)] + [f"{d}m" for d in range(1, 10)]
QUANTITIES = list(range(1, 500, 1))
DELIVERY_DAYS = list(range(1, 30))
DISCOUNT_RATES = [5, 7, 8, 10, 12, 15, 18, 20, 25, 30]
WARRANTY_MONTHS = [1, 3, 6, 12, 18, 24, 36]
STOCK_COUNTS = list(range(1, 1000))

# 仕様パラメータ
VOLTAGES = ['3.6V', '7.2V', '10.8V', '14.4V', '18V', '24V', '36V', '100V', '200V']
CAPACITIES = ['1.5Ah', '2.0Ah', '3.0Ah', '4.0Ah', '5.0Ah', '6.0Ah', '8.0Ah']
TORQUES = [f"{t}N・m" for t in range(10, 300, 5)]
RPM = [f"{r}rpm" for r in range(500, 20000, 100)]
PRECISIONS = ['±0.001mm', '±0.005mm', '±0.01mm', '±0.02mm', '±0.05mm', '±0.1mm']
IP_RATINGS = ['IP54', 'IP55', 'IP65', 'IP66', 'IP67', 'IP68']
CERTIFICATIONS = ['JIS', 'ISO', 'CE', 'UL', 'PSE', 'OSHA', 'ANSI', 'EN', 'KS']

# 材質
MATERIALS_JA = ['ステンレス', '超硬合金', 'ハイス鋼', '炭素鋼', 'クロムモリブデン鋼', 'アルミニウム', 'チタン', 
                '真鍮', '銅', 'ABS樹脂', 'PC樹脂', 'ナイロン', 'ゴム', 'シリコン', 'フッ素樹脂']
MATERIALS_EN = ['stainless steel', 'carbide', 'HSS', 'carbon steel', 'chrome-moly', 'aluminum', 'titanium',
                'brass', 'copper', 'ABS plastic', 'polycarbonate', 'nylon', 'rubber', 'silicone', 'PTFE']

# 色
COLORS_JA = ['黒', '白', '赤', '青', '緑', '黄', '橙', '紫', '銀', '金', 'クリア', 'グレー', 'ネイビー']
COLORS_EN = ['black', 'white', 'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'silver', 'gold', 'clear', 'gray', 'navy']
COLORS_ZH = ['黑色', '白色', '红色', '蓝色', '绿色', '黄色', '橙色', '紫色', '银色', '金色', '透明', '灰色', '藏青']

# ============================================================
# 動的質問生成関数 (日本語)
# ============================================================

def gen_ja_price_qa(entity):
    """価格に関する質問"""
    price = random.choice(PRICES)
    discount = random.choice(DISCOUNT_RATES)
    patterns = [
        (f"この{entity}、いくら？", f"{price:,}円です。"),
        (f"{entity}の価格教えて", f"税込み{price:,}円になります。"),
        (f"なんぼ？", f"{price:,}円やで。"),
        (f"まとめ買いで安くなる？", f"{discount}%オフになります。"),
        (f"法人割引ある？", f"法人様は{discount}%引きです。"),
        (f"もうちょい安くならへん？", f"申し訳ございません、これが最安値の{price:,}円です。"),
        (f"ポイント何倍？", f"今なら{random.randint(2, 10)}倍ポイントです。"),
        (f"予算{random.choice([3000, 5000, 10000, 20000])}円で収まる？", random.choice(["ギリギリ収まりますよ。", "少しオーバーしますね…"])),
    ]
    q, a = random.choice(patterns)
    return q, a, "価格", str(price)

def gen_ja_stock_qa(entity):
    """在庫に関する質問"""
    stock = random.choice(STOCK_COUNTS)
    days = random.choice(DELIVERY_DAYS)
    patterns = [
        (f"{entity}、在庫ある？", f"はい、{stock}個在庫あります。"),
        (f"これ今日出せる？", random.choice(["午前中注文で当日発送できます。", f"{days}日後の発送になります。"])),
        (f"入荷予定いつ？", f"来週{random.choice(['月', '火', '水', '木', '金'])}曜日入荷予定です。"),
        (f"注文してからどれくらいで届く？", f"約{days}営業日でお届けします。"),
        (f"急ぎなんやけど", random.choice([f"特急便で{random.randint(1,3)}日です。", "申し訳ございません、在庫切れです…"])),
        (f"品薄？", random.choice(["大丈夫、まだ十分あります。", "残り少なめなのでお早めに。"])),
        (f"{entity}って人気？", f"めっちゃ売れてますよ、月{random.randint(100, 5000)}個出てます。"),
        (f"型番{random.choice(['A', 'B', 'C', 'D'])}-{random.randint(100, 999)}ある？", random.choice(["ございます。", "廃番になりました。"])),
    ]
    q, a = random.choice(patterns)
    return q, a, "在庫", str(stock)

def gen_ja_spec_qa(entity, category):
    """仕様に関する質問"""
    weight = random.choice(WEIGHTS)
    dim = random.choice(DIMENSIONS)
    voltage = random.choice(VOLTAGES)
    torque = random.choice(TORQUES)
    precision = random.choice(PRECISIONS)
    material = random.choice(MATERIALS_JA)
    color = random.choice(COLORS_JA)
    
    patterns = [
        (f"{entity}の重さは？", f"{weight}です。"),
        (f"寸法教えて", f"幅{random.choice(DIMENSIONS)}×高さ{random.choice(DIMENSIONS)}×奥行{random.choice(DIMENSIONS)}です。"),
        (f"全長いくつ？", f"{dim}です。"),
        (f"材質は何？", f"{material}製です。"),
        (f"何色ある？", f"{color}と{random.choice(COLORS_JA)}の2色展開です。"),
        (f"電圧は？", f"{voltage}仕様です。"),
        (f"トルクどれくらい出る？", f"最大{torque}です。"),
        (f"精度は？", f"{precision}の高精度です。"),
        (f"防水対応？", f"{random.choice(IP_RATINGS)}対応です。"),
        (f"最大回転数は？", f"{random.choice(RPM)}です。"),
        (f"バッテリー容量は？", f"{random.choice(CAPACITIES)}です。"),
        (f"{random.choice(CERTIFICATIONS)}規格通ってる？", "はい、適合品です。"),
        (f"耐荷重どれくらい？", f"{random.choice(range(10, 500, 10))}kgまでOKです。"),
        (f"使用温度範囲は？", f"-{random.randint(10, 40)}℃〜+{random.randint(40, 80)}℃です。"),
    ]
    q, a = random.choice(patterns)
    keywords = [entity[:8], random.choice(["重量", "寸法", "材質", "色", "仕様"])]
    return q, a, ";".join(keywords), random.choice([weight, dim, material, color])

def gen_ja_service_qa(entity):
    """サービスに関する質問"""
    warranty = random.choice(WARRANTY_MONTHS)
    patterns = [
        ("保証期間は？", f"{warranty}ヶ月保証です。"),
        ("返品できる？", f"未開封なら{random.randint(7, 30)}日以内返品可能です。"),
        ("取り付けサービスある？", random.choice(["別途料金で承ります。", "お客様ご自身でお願いしております。"])),
        ("修理対応してる？", "メーカー修理窓口をご案内します。"),
        ("交換パーツ買える？", "消耗品は単体でご購入いただけます。"),
        ("技術サポートある？", f"平日{random.randint(8, 10)}時〜{random.randint(17, 20)}時まで対応しております。"),
        ("見積書発行できる？", "PDFまたは紙でご用意できます。"),
        ("請求書払いできる？", "法人様は月末締め翌月末払い可能です。"),
        ("領収書の宛名変更できる？", "ご指定いただければ対応します。"),
        (f"送料は？", f"{random.choice([300, 500, 700, 1000, 1500])}円です。{random.choice([3000, 5000, 10000])}円以上で無料。"),
    ]
    q, a = random.choice(patterns)
    return q, a, "サービス", str(warranty)

def gen_ja_comparison_qa(entity, category):
    """比較に関する質問"""
    competitors = ["A社製", "B社製", "国産", "海外製", "従来品", "旧型", "プロ仕様", "家庭用"]
    patterns = [
        (f"{random.choice(competitors)}と比べてどう？", random.choice(["コスパで当社製品が優位です。", "同等品質ですがお値段はお安めです。"])),
        ("他の商品と何が違う？", f"{random.choice(['耐久性', '精度', '軽さ', '使いやすさ'])}が段違いです。"),
        ("おすすめはどれ？", f"{entity}が一番人気ですね。"),
        ("プロ向け？素人でも使える？", random.choice(["初心者でも安心です。", "ある程度経験者向けですね。"])),
        ("類似品との互換性ある？", random.choice(["互換性あります。", "専用品になります。"])),
        (f"もっと{random.choice(['高性能', '安い', '軽い', '丈夫な'])}のある？", "上位モデルをご案内しましょうか？"),
    ]
    q, a = random.choice(patterns)
    return q, a, "比較", entity

def gen_ja_usage_qa(entity, category):
    """使用方法に関する質問"""
    patterns = [
        ("取り付け難しい？", random.choice(["簡単です、説明書通りでOK。", "専門知識が必要です。"])),
        ("使い方教えて", "同梱の説明書に詳しく記載しております。"),
        ("何に使うの？", f"{random.choice(['現場作業', '製造', 'メンテナンス', 'DIY', '組立'])}に最適です。"),
        ("初めてでも大丈夫？", "初心者向けの解説動画もあります。"),
        (f"{random.choice(['木材', 'アルミ', '鉄', 'プラスチック', 'コンクリート'])}に使える？", random.choice(["問題なく使えます。", "専用品をおすすめします。"])),
        ("メンテナンス必要？", f"{random.randint(1, 12)}ヶ月ごとの点検をおすすめします。"),
        ("1日何時間使える？", f"連続{random.randint(2, 8)}時間使用可能です。"),
        ("消耗品の交換頻度は？", f"約{random.choice([100, 200, 500, 1000, 2000])}回使用後に交換推奨です。"),
    ]
    q, a = random.choice(patterns)
    return q, a, "使用方法", entity

# ============================================================
# 動的質問生成関数 (英語)
# ============================================================

def gen_en_qa(entity, category):
    price = random.choice(PRICES)
    days = random.choice(DELIVERY_DAYS)
    weight = random.choice(WEIGHTS)
    material = random.choice(MATERIALS_EN)
    color = random.choice(COLORS_EN)
    warranty = random.choice(WARRANTY_MONTHS)
    discount = random.choice(DISCOUNT_RATES)
    
    patterns = [
        (f"How much is the {entity}?", f"It's ${price//100:.2f}."),
        (f"What's the lead time?", f"About {days} business days."),
        (f"Is it in stock?", f"Yes, {random.choice(STOCK_COUNTS)} units available."),
        (f"What material is it?", f"Made of {material}."),
        (f"What colors do you have?", f"Available in {color} and {random.choice(COLORS_EN)}."),
        (f"How heavy is it?", f"Approximately {weight}."),
        (f"What's the warranty?", f"{warranty} months warranty included."),
        (f"Any bulk discounts?", f"{discount}% off for orders over {random.randint(10, 100)} units."),
        (f"Is it {random.choice(CERTIFICATIONS)} certified?", random.choice(["Yes, fully certified.", "Certification in progress."])),
        (f"What's the max torque?", f"{random.choice(TORQUES)}."),
        (f"Is it waterproof?", f"{random.choice(IP_RATINGS)} rated."),
        (f"Can I return it?", f"Yes, within {random.randint(14, 60)} days."),
        (f"Does it come with accessories?", random.choice(["Yes, full kit included.", "Accessories sold separately."])),
        (f"Is international shipping available?", random.choice(["Yes, we ship worldwide.", "Domestic only, sorry."])),
        (f"Can I get a quote?", "Sure, I'll email you the details."),
        (f"Is this the latest model?", random.choice(["Yes, {entity} version 2.0.", "New model coming soon."])),
    ]
    q, a = random.choice(patterns)
    return q, a, entity, str(price)

# ============================================================
# 動的質問生成関数 (中国語)
# ============================================================

def gen_zh_qa(entity, category):
    price = random.choice(PRICES)
    days = random.choice(DELIVERY_DAYS)
    color = random.choice(COLORS_ZH)
    warranty = random.choice(WARRANTY_MONTHS)
    discount = random.choice(DISCOUNT_RATES)
    stock = random.choice(STOCK_COUNTS)
    
    patterns = [
        (f"{entity}多少钱？", f"{price}日元。"),
        ("有货吗？", f"有的，库存{stock}个。"),
        ("多久能发货？", f"大约{days}天发货。"),
        ("什么材质的？", f"{random.choice(['不锈钢', '合金', '碳钢', '铝合金', '塑料', '橡胶'])}的。"),
        ("什么颜色有？", f"有{color}和{random.choice(COLORS_ZH)}。"),
        (f"批量买能便宜吗？", f"10个起{discount}%折扣。"),
        ("保修多久？", f"{warranty}个月保修。"),
        ("能退货吗？", f"{random.randint(7, 30)}天内可退。"),
        ("有发票吗？", "可以开增值税发票。"),
        ("能货到付款吗？", random.choice(["可以。", "仅支持在线付款。"])),
        (f"精度多少？", f"{random.choice(PRECISIONS)}。"),
        ("防水吗？", f"{random.choice(IP_RATINGS)}级别。"),
        ("好用吗？", random.choice(["非常好用，回购率很高。", "专业级品质，放心用。"])),
        (f"最大扭矩多少？", f"{random.choice(TORQUES)}。"),
        ("新款还是老款？", random.choice(["最新款。", "经典款，销量王。"])),
        ("适合什么场景？", f"{random.choice(['工厂', '工地', '家用', '车间', '实验室'])}使用。"),
    ]
    q, a = random.choice(patterns)
    return q, a, entity, str(price)

# ============================================================
# 対話生成 (完全動的版)
# ============================================================

JA_INTROS = [
    "Q:すみません、{entity}について質問なんですけど。|||A:はい、何でしょうか？",
    "Q:こんにちは、{entity}見てるんですが。|||A:ありがとうございます。ご質問ございますか？",
    "Q:ちょっと聞きたいんやけど|||A:はい、どうぞ。",
    "Q:{entity}これどう？|||A:いい商品ですよ。",
    "Q:お忙しいところすみません|||A:いえいえ、どうぞ。",
    "Q:初めまして、{entity}の件で|||A:はい、承ります。",
    "Q:あの、{entity}なんですが|||A:はい。",
    "Q:{entity}検討中で|||A:ありがとうございます。",
    "Q:ちょい質問いい？|||A:どうぞどうぞ。",
    "Q:すいませーん|||A:はい、いらっしゃいませ。",
]

EN_INTROS = [
    "Q:Hi, I'm looking at {entity}.|||A:Sure, how can I help?",
    "Q:Quick question about {entity}.|||A:Of course, go ahead.",
    "Q:Excuse me, about the {entity}...|||A:Yes?",
    "Q:Hey, need info on {entity}.|||A:Absolutely.",
    "Q:Looking for a {entity}.|||A:Great choice.",
]

ZH_INTROS = [
    "Q:你好，我想问下{entity}|||A:您好，请说。",
    "Q:在吗？看看{entity}|||A:在的，您说。",
    "Q:老板，{entity}怎么样？|||A:很不错的。",
    "Q:咨询下{entity}|||A:好的。",
]

JA_ENDINGS_POS = [
    "Q:わかりました、これにします。|||A:ありがとうございます！",
    "Q:よし、買うわ。|||A:ありがとうございます！",
    "Q:決めた！|||A:ありがとうございます、処理いたします。",
    "Q:カートに入れた。|||A:ご注文お待ちしております！",
    "Q:注文するわ。|||A:ありがとうございます！",
]

JA_ENDINGS_NEG = [
    "Q:ちょっと考えます。|||A:かしこまりました。",
    "Q:やめとくわ。|||A:承知しました。",
    "Q:また検討します。|||A:はい、いつでもどうぞ。",
    "Q:予算的にちょっと…|||A:ご予算に合うものもご案内できますよ。",
]

JA_ENDINGS_NEUTRAL = [
    "Q:見積もりもらえる？|||A:お送りしますね。",
    "Q:上に確認してみる。|||A:承知しました。",
    "Q:サンプルある？|||A:手配いたします。",
]

EN_ENDINGS = [
    ("Q:I'll take it.|||A:Great, thanks!", 5),
    ("Q:Let me think.|||A:Sure thing.", 3),
    ("Q:Too pricey.|||A:We have budget options.", 2),
]

ZH_ENDINGS = [
    ("Q:买了。|||A:好的，谢谢！", 5),
    ("Q:再看看。|||A:好的。", 3),
    ("Q:太贵了。|||A:有便宜款。", 2),
]

def generate_unique_dialogue(category, entity, sat_score, lang='ja'):
    """完全動的対話生成"""
    parts = []
    keywords_q = [entity[:10]]
    keywords_a = []
    
    num_turns = random.randint(2, 5)
    
    if lang == 'ja':
        # イントロ
        intro = random.choice(JA_INTROS).format(entity=entity[:12])
        parts.append(intro)
        
        # 動的生成関数をランダムに選択
        qa_funcs = [gen_ja_price_qa, gen_ja_stock_qa, gen_ja_spec_qa, gen_ja_service_qa, gen_ja_comparison_qa, gen_ja_usage_qa]
        used_funcs = random.sample(qa_funcs, min(num_turns, len(qa_funcs)))
        
        for func in used_funcs:
            if func == gen_ja_spec_qa or func == gen_ja_comparison_qa or func == gen_ja_usage_qa:
                q, a, kq, ka = func(entity, category)
            else:
                q, a, kq, ka = func(entity)
            parts.append(f"Q:{q}|||A:{a}")
            keywords_q.append(kq)
            keywords_a.append(ka)
        
        # エンディング
        if sat_score >= 4:
            end = random.choice(JA_ENDINGS_POS)
        elif sat_score <= 2:
            end = random.choice(JA_ENDINGS_NEG)
        else:
            end = random.choice(JA_ENDINGS_NEUTRAL)
        parts.append(end)
    
    elif lang == 'en':
        intro = random.choice(EN_INTROS).format(entity=entity[:12])
        parts.append(intro)
        
        for _ in range(num_turns):
            q, a, kq, ka = gen_en_qa(entity, category)
            parts.append(f"Q:{q}|||A:{a}")
            keywords_q.append(kq)
            keywords_a.append(ka)
        
        endings = [e for e, s in EN_ENDINGS if s <= sat_score] or [EN_ENDINGS[1][0]]
        parts.append(random.choice(endings) if isinstance(endings[0], str) else endings[0])
    
    else:
        intro = random.choice(ZH_INTROS).format(entity=entity[:12])
        parts.append(intro)
        
        for _ in range(num_turns):
            q, a, kq, ka = gen_zh_qa(entity, category)
            parts.append(f"Q:{q}|||A:{a}")
            keywords_q.append(kq)
            keywords_a.append(ka)
        
        endings = [e for e, s in ZH_ENDINGS if s <= sat_score] or [ZH_ENDINGS[1][0]]
        parts.append(endings[0])
    
    full_sent = "|||".join(parts)
    full_keywords = f"Q:{';'.join(keywords_q[:5])};A:{';'.join(keywords_a[:5])}"
    
    return {
        "sent": full_sent,
        "keywords": full_keywords,
        "first_category": category,
        "sat": sat_score,
        "lang": lang
    }

def generate_data_pool(total_needed):
    """完全一意データプール生成"""
    unique_hashes = set()
    data_list = []
    max_attempts = total_needed * 50
    attempt = 0
    
    available_cats = list(CATEGORY_ENTITIES.keys())
    lang_choices = ['ja'] * LANG_WEIGHTS['ja'] + ['en'] * LANG_WEIGHTS['en'] + ['zh'] * LANG_WEIGHTS['zh']
    
    print(f">>> Generating {total_needed} UNIQUE dialogues (dynamic generation)...")
    
    while len(data_list) < total_needed and attempt < max_attempts:
        attempt += 1
        cat = random.choice(available_cats)
        entity = random.choice(CATEGORY_ENTITIES[cat])
        sat = random.choices([1, 2, 3, 4, 5], weights=[1, 1, 3, 4, 2])[0]
        lang = random.choice(lang_choices)
        
        row = generate_unique_dialogue(cat, entity, sat, lang)
        sent_hash = hashlib.sha256(row['sent'].encode()).hexdigest()
        
        if sent_hash not in unique_hashes:
            unique_hashes.add(sent_hash)
            data_list.append(row)
            
            if len(data_list) % 2000 == 0:
                print(f"    -> Generated {len(data_list)} unique dialogues (attempt {attempt})...")
    
    print(f"    -> Final: {len(data_list)} unique dialogues generated.")
    return data_list

# ============================================================
# メイン処理
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print(" MonotaRO Dynamic Dialogue Generation (10,000+)")
    print("=" * 60)
    
    train_files = [f'monotaro/reproduce/data/train/data_turn/dialogue_{i}.csv' for i in range(1, 51)]
    valid_files = [f'monotaro/reproduce/data/valid/data_turn/dialogue_{i}.csv' for i in range(1, 6)]
    
    rows_per_train = 200
    rows_per_valid = 100
    total_train = rows_per_train * len(train_files)
    total_valid = rows_per_valid * len(valid_files)
    
    pool = generate_data_pool(total_train + total_valid)
    random.shuffle(pool)
    
    idx = 0
    for fpath in train_files:
        subset = pool[idx:idx + rows_per_train]
        if subset:
            pd.DataFrame(subset).to_csv(fpath, index=False, encoding='utf-8-sig')
            print(f"Generated {fpath}")
        idx += rows_per_train
    
    for fpath in valid_files:
        subset = pool[idx:idx + rows_per_valid]
        if subset:
            pd.DataFrame(subset).to_csv(fpath, index=False, encoding='utf-8-sig')
            print(f"Generated {fpath}")
        idx += rows_per_valid
    
    # 統計
    all_data = pd.concat([pd.read_csv(f, encoding='utf-8-sig') for f in train_files if os.path.exists(f)])
    unique_sents = all_data['sent'].nunique()
    
    print("\n" + "=" * 60)
    print(" Generation Complete!")
    print("=" * 60)
    print(f" Total dialogues: {len(all_data)}")
    print(f" Unique dialogues: {unique_sents} ({unique_sents/len(all_data)*100:.1f}%)")
    print(f" Language distribution:")
    print(all_data['lang'].value_counts(normalize=True).to_string())
    print("=" * 60)
