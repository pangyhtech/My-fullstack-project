# -*- coding: utf-8 -*-
"""
MonotaRO 知識グラフ資産生成スクリプト (完全版)
実際の商品名・属性・関係を使用した一意データ生成
"""

import os
import pickle
import pandas as pd
import torch
import numpy as np
import csv
from monotaro_categories import CATEGORY_ENTITIES, CATEGORY_LIST, CATEGORY_RELATIONS

# ディレクトリ作成
os.makedirs('monotaro/KG_tail_prediction/data/Entity_linking', exist_ok=True)
os.makedirs('monotaro/KG_tail_prediction/data/E&R', exist_ok=True)
os.makedirs('monotaro/KG_tail_prediction/data/relations_for_different_category', exist_ok=True)
os.makedirs('monotaro/KG_tail_prediction/model', exist_ok=True)

print("=" * 60)
print(" MonotaRO KG Asset Generation (Full Version)")
print("=" * 60)

# ============================================================
# 1. 実際のエンティティ詳細データ
# ============================================================

# 商品ごとの詳細属性 (一意の説明テキスト)
ENTITY_DETAILS = {
    # 安全保護具・作業服・安全靴
    "ヘルメット": {"材質": "ABS樹脂", "重量": "340g", "規格": "JIS T8131", "特徴": "通気孔6個、飛来落下物用"},
    "安全靴": {"材質": "牛革/ゴム底", "規格": "JIS T8101", "特徴": "鋼製先芯、耐油性"},
    "安全帯": {"規格": "厚労省規格適合", "特徴": "フルハーネス型、墜落制止用"},
    "防護メガネ": {"材質": "ポリカーボネート", "規格": "JIS T8147", "特徴": "曇り止め加工"},
    "作業手袋": {"材質": "ニトリルゴム", "サイズ": "S/M/L/LL", "特徴": "耐油・耐薬品性"},
    "防塵マスク": {"規格": "DS2", "特徴": "区分2、使い捨て式"},
    "イヤーマフ": {"NRR": "25dB", "特徴": "折りたたみ式"},
    "保護キャップ": {"材質": "PE", "特徴": "軽量インナーキャップ"},
    "防水作業着": {"材質": "ポリエステル", "耐水圧": "10,000mm", "透湿性": "3,000g/m²"},
    "安全ベスト": {"材質": "メッシュ", "反射材": "360度反射", "色": "蛍光イエロー"},
    
    # 切削工具・研磨材
    "ドリルビット": {"材質": "超硬合金", "径": "3-13mm", "コーティング": "TiAlN"},
    "エンドミル": {"材質": "ハイス", "刃数": "2-4枚", "精度": "±0.02mm"},
    "タップ": {"材質": "HSS-E", "ピッチ": "M3-M12", "形式": "スパイラル"},
    "砥石": {"材質": "WA", "粒度": "#60-#3000", "結合剤": "ビトリファイド"},
    "バイト": {"材質": "超硬チップ", "角度": "80°", "用途": "旋盤加工"},
    "リーマ": {"精度": "H7", "材質": "超硬", "形状": "ストレート"},
    "ヤスリ": {"材質": "炭素工具鋼", "目": "中目/細目", "長さ": "150-300mm"},
    "研磨ベルト": {"粒度": "#40-#400", "幅": "10-100mm", "材質": "アルミナ"},
    "バフ": {"材質": "綿布", "径": "100-200mm", "用途": "鏡面仕上げ"},
    "ホルダー": {"シャンク": "φ16-32mm", "規格": "BT30/40", "特徴": "高精度"},
    
    # 測定・測量用品
    "ノギス": {"精度": "0.01mm", "材質": "ステンレス", "測定範囲": "0-150mm"},
    "マイクロメータ": {"精度": "0.001mm", "測定範囲": "0-25mm", "方式": "デジタル"},
    "ダイヤルゲージ": {"精度": "0.01mm", "測定範囲": "10mm", "直径": "φ57mm"},
    "水準器": {"精度": "0.05mm/m", "長さ": "300-1200mm", "材質": "アルミ"},
    "レーザー距離計": {"精度": "±1.5mm", "測定範囲": "0.05-100m", "防塵防水": "IP54"},
    "照度計": {"測定範囲": "0-200,000lx", "精度": "±3%", "センサー": "シリコンフォトダイオード"},
    "騒音計": {"測定範囲": "30-130dB", "精度": "±1.5dB", "規格": "IEC 61672 Class2"},
    "回転計": {"測定範囲": "2.5-99,999rpm", "方式": "非接触光学式"},
    "厚さ計": {"測定範囲": "0.8-300mm", "精度": "±(1%H+0.1mm)", "方式": "超音波式"},
    "放射温度計": {"測定範囲": "-50~500℃", "精度": "±1.5%", "放射率": "0.1-1.0可変"},
    
    # 作業工具/電動・空圧工具
    "インパクトドライバー": {"電圧": "18V", "トルク": "180N・m", "バッテリー": "5.0Ah"},
    "電動ドリル": {"回転数": "0-2800rpm", "電圧": "14.4V", "チャック": "10mm"},
    "グラインダー": {"砥石径": "100mm", "回転数": "12,000rpm", "電力": "720W"},
    "丸のこ": {"刃径": "165mm", "切込み深さ": "66mm", "電圧": "18V"},
    "ジグソー": {"ストローク": "26mm", "切断能力": "木材135mm", "電圧": "18V"},
    "電動のこぎり": {"刃長": "150mm", "ストローク数": "0-3000spm", "電力": "1010W"},
    "ハンマードリル": {"電圧": "18V", "穿孔径": "コンクリート28mm", "打撃数": "5100bpm"},
    "ニッパー": {"材質": "クロムバナジウム鋼", "刃長": "125mm", "切断能力": "φ2.6mm"},
    "ラチェットレンチ": {"サイズ": "8-24mm", "歯数": "72", "材質": "クロムモリブデン"},
    "トルクレンチ": {"範囲": "10-100N・m", "精度": "±3%", "目盛": "1N・m"},
    
    # 自動車用品
    "エンジンオイル": {"粘度": "5W-30", "規格": "API SP", "容量": "4L"},
    "タイヤ": {"サイズ": "195/65R15", "荷重指数": "91", "速度記号": "V"},
    "バッテリー": {"電圧": "12V", "容量": "55Ah", "サイズ": "B24"},
    "ワイパー": {"長さ": "450/400mm", "形式": "エアロタイプ"},
    "エアフィルター": {"適合車種": "車種別設定", "交換目安": "20,000km"},
    "ブレーキパッド": {"材質": "セミメタリック", "適合": "純正互換"},
    "ヘッドライト": {"形式": "LED", "全光束": "6000lm", "色温度": "6500K"},
    "カーナビ": {"画面": "9インチ", "解像度": "WVGA", "HDMI": "対応"},
    "ドライブレコーダー": {"解像度": "2K", "視野角": "170°", "駐車監視": "対応"},
    "ブースターケーブル": {"容量": "100A", "長さ": "3.5m", "適合": "12V/24V"},
    
    # 配管・水廻り部材
    "塩ビ管": {"規格": "VU/VP", "径": "50-150mm", "材質": "硬質ポリ塩化ビニル"},
    "継手": {"種類": "エルボ/チーズ/ソケット", "材質": "HIVP", "接合": "TS接合"},
    "バルブ": {"種類": "ボール弁", "口径": "15A-50A", "材質": "青銅"},
    "ポンプ": {"種類": "渦巻ポンプ", "揚程": "10-50m", "吐出量": "50-200L/min"},
    "ホース": {"材質": "軟質塩ビ", "内径": "15-50mm", "耐圧": "0.5MPa"},
    "水栓": {"種類": "シングルレバー", "材質": "黄銅", "取付": "ワンホール"},
    "電磁弁": {"作動圧力": "0-0.5MPa", "流体温度": "5-60℃", "電圧": "AC100V"},
    "エアシリンダ": {"内径": "20-63mm", "ストローク": "25-300mm", "作動圧力": "0.1-1.0MPa"},
    "レギュレータ": {"設定圧力": "0.05-0.85MPa", "流量": "1500L/min", "接続": "G1/4"},
    "フィルター": {"ろ過精度": "5μm", "流量": "500L/min", "材質": "ろ過エレメント焼結金属"},
    
    # 医療・介護用品
    "マスク": {"規格": "サージカル", "材質": "不織布3層", "サイズ": "175×95mm"},
    "手袋": {"材質": "ニトリル", "サイズ": "S/M/L", "特徴": "パウダーフリー"},
    "消毒液": {"成分": "エタノール76.9-81.4vol%", "容量": "500mL", "形態": "ポンプ式"},
    "体温計": {"方式": "非接触", "測定時間": "1秒", "精度": "±0.2℃"},
    "血圧計": {"方式": "オシロメトリック", "測定範囲": "0-299mmHg", "メモリ": "60回分"},
    "車椅子": {"座幅": "40cm", "重量": "12.5kg", "耐荷重": "100kg"},
    "パルスオキシメーター": {"測定範囲": "SpO2 70-100%", "脈拍": "30-250bpm", "精度": "±2%"},
    "聴診器": {"チェストピース": "ダブル", "チューブ長": "70cm", "重量": "122g"},
    "注射器": {"容量": "1-50mL", "材質": "PP", "針": "別売り"},
    "包帯": {"材質": "伸縮綿", "幅": "5-10cm", "長さ": "4.5m"},
}

# ============================================================
# 2. 実際の関係データ (カテゴリ別)
# ============================================================

RELATION_TYPES = {
    "安全保護具・作業服・安全靴": [
        ("適合規格", "JIS/CE/ANSI等の安全規格への適合状態"),
        ("保護等級", "防護性能のレベル"),
        ("サイズ展開", "利用可能なサイズバリエーション"),
        ("重量", "装着時の重さ"),
        ("素材", "使用されている主要素材"),
        ("耐用年数", "推奨交換時期"),
        ("装着部位", "身体のどの部位を保護するか"),
        ("使用環境", "推奨される作業環境"),
    ],
    "切削工具・研磨材": [
        ("加工対象", "切削可能な材質"),
        ("刃先形状", "切れ刃の幾何学的形状"),
        ("コーティング", "表面処理の種類"),
        ("シャンク径", "取り付け部の直径"),
        ("刃数", "切れ刃の枚数"),
        ("切削速度", "推奨回転数/送り速度"),
        ("精度等級", "加工精度のグレード"),
        ("寿命", "交換までの目安加工数"),
    ],
    "測定・測量用品": [
        ("測定範囲", "計測可能な最小/最大値"),
        ("分解能", "読取可能な最小単位"),
        ("確度", "真値との誤差範囲"),
        ("繰返し精度", "同一条件での再現性"),
        ("校正周期", "推奨キャリブレーション間隔"),
        ("動作環境", "使用可能な温度/湿度"),
        ("データ出力", "PC/スマホ連携機能"),
        ("防水等級", "IP規格"),
    ],
    "作業工具/電動・空圧工具": [
        ("定格電圧", "バッテリー/電源電圧"),
        ("最大トルク", "締付け/穿孔トルク"),
        ("回転数", "無負荷回転速度"),
        ("バッテリー容量", "Ah数"),
        ("連続作業時間", "満充電時の稼働時間"),
        ("重量", "バッテリー込み重量"),
        ("振動値", "手-腕振動値"),
        ("騒音レベル", "作業時のdB値"),
    ],
    "自動車用品": [
        ("適合車種", "装着可能な車種/年式"),
        ("純正番号", "OEM品番との互換性"),
        ("サイズ", "寸法/容量"),
        ("規格", "JIS/SAE等の規格"),
        ("交換周期", "推奨交換タイミング"),
        ("性能", "出力/効率"),
        ("取付方式", "DIY可否"),
        ("保証期間", "メーカー保証"),
    ],
    "医療・介護用品": [
        ("医療機器クラス", "医療機器分類"),
        ("滅菌方法", "EOG/γ線/未滅菌"),
        ("使用期限", "開封前の保存可能期間"),
        ("介護保険適用", "保険給付対象か"),
        ("衛生管理", "単回使用/再使用可"),
        ("アレルギー対応", "ラテックス/パウダーフリー"),
        ("精度", "測定の正確さ"),
        ("容量・サイズ", "1回分の量や寸法"),
    ],
}

# ============================================================
# 3. 資産ファイル生成
# ============================================================

print(">>> [1/5] Generating product_to_entity_examples.csv...")

rows = []
ent_id = 1
for cat in CATEGORY_LIST:
    if cat not in CATEGORY_ENTITIES:
        continue
    products = CATEGORY_ENTITIES[cat]
    row = [cat, "DefaultSub"]
    for product in products:
        row.extend([product, f"ent_{ent_id}"])
        ent_id += 1
    # パディング
    while len(row) < 44:
        row.append("")
    rows.append(row)

with open('monotaro/KG_tail_prediction/data/Entity_linking/product_to_entity_examples.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"    -> {len(rows)} categories, {ent_id - 1} entities")

# ============================================================
# 4. 一意のエンティティ詳細CSV
# ============================================================

print(">>> [2/5] Generating entity_examples.csv with UNIQUE descriptions...")

entity_rows = []
ent_id = 1
for cat in CATEGORY_LIST:
    if cat not in CATEGORY_ENTITIES:
        continue
    products = CATEGORY_ENTITIES[cat]
    for product in products:
        # 商品固有の説明を生成
        if product in ENTITY_DETAILS:
            details = ENTITY_DETAILS[product]
            desc_parts = [f"{k}:{v}" for k, v in details.items()]
            description = f"{product} - " + ", ".join(desc_parts)
        else:
            # 詳細がない場合はカテゴリ情報を含める
            description = f"{product} ({cat}) - 工業用品、品質保証付き、即日発送対応"
        
        entity_rows.append({
            "id": ent_id,
            "entity": f"ent_{ent_id}",
            "name": product,
            "category": cat,
            "text": description
        })
        ent_id += 1

df_entities = pd.DataFrame(entity_rows)
df_entities.to_csv('monotaro/KG_tail_prediction/data/E&R/entity_examples.csv', index=False, encoding='utf-8-sig')
print(f"    -> {len(entity_rows)} unique entity descriptions")

# ============================================================
# 5. 一意の関係詳細CSV
# ============================================================

print(">>> [3/5] Generating relation_examples.csv with UNIQUE relations...")

relation_rows = []
rel_id = 1

# 汎用関係（全カテゴリ共通）
generic_relations = [
    ("価格", "製品の販売価格（税込/税抜）"),
    ("在庫状況", "現在の在庫有無と数量"),
    ("納期", "注文から届くまでの日数"),
    ("送料", "配送にかかる費用"),
    ("メーカー", "製造元の会社名"),
    ("型番", "製品の識別番号"),
    ("重量", "製品の質量"),
    ("寸法", "製品の外形サイズ"),
    ("材質", "使用されている素材"),
    ("色", "製品の色・カラーバリエーション"),
    ("保証期間", "メーカー保証の有効期間"),
    ("返品条件", "返品・交換の条件"),
    ("評価", "ユーザーレビューの評点"),
    ("販売実績", "累計販売数・人気度"),
    ("関連商品", "一緒に購入されることの多い製品"),
]

for rel_name, rel_desc in generic_relations:
    relation_rows.append({
        "id": rel_id,
        "relation": f"rel_{rel_id}",
        "name": rel_name,
        "category": "共通",
        "text": rel_desc
    })
    rel_id += 1

# カテゴリ固有の関係
for cat, relations in RELATION_TYPES.items():
    for rel_name, rel_desc in relations:
        relation_rows.append({
            "id": rel_id,
            "relation": f"rel_{rel_id}",
            "name": rel_name,
            "category": cat,
            "text": f"{cat}向け: {rel_desc}"
        })
        rel_id += 1

df_relations = pd.DataFrame(relation_rows)
df_relations.to_csv('monotaro/KG_tail_prediction/data/E&R/relation_examples.csv', index=False, encoding='utf-8-sig')
print(f"    -> {len(relation_rows)} unique relation definitions")

# ============================================================
# 6. カテゴリテーブル (pickle)
# ============================================================

print(">>> [4/5] Generating category_table.pickle...")

category_table = {}
for i, cat in enumerate(CATEGORY_LIST):
    if cat in CATEGORY_ENTITIES:
        products = CATEGORY_ENTITIES[cat]
        category_table[cat] = {
            "id": i,
            "entities": products,
            "entity_ids": [f"ent_{j+1}" for j in range(i*20, i*20+len(products))],
            "relations": CATEGORY_RELATIONS.get(cat, ["価格", "在庫", "納期", "品質"]),
        }

with open('monotaro/KG_tail_prediction/data/relations_for_different_category/category_table.pickle', 'wb') as f:
    pickle.dump(category_table, f)

print(f"    -> {len(category_table)} categories with entity/relation mappings")

# ============================================================
# 7. カテゴリ別関係マッピング (pickle)
# ============================================================

print(">>> [5/5] Generating category_refined_rel_new.pkl...")

category_rel_map = {}
for cat in CATEGORY_LIST:
    if cat in CATEGORY_RELATIONS:
        category_rel_map[cat] = CATEGORY_RELATIONS[cat]
    else:
        category_rel_map[cat] = ["価格", "在庫", "品質", "納期"]

with open('monotaro/KG_tail_prediction/data/relations_for_different_category/category_refined_rel_new.pkl', 'wb') as f:
    pickle.dump(category_rel_map, f)

# ============================================================
# 8. TuckER モデル (ダミー)
# ============================================================

print(">>> [BONUS] Generating TuckER_model.pkl (dummy weights)...")

class DummyTuckER:
    def __init__(self, num_entities, num_relations, d=200):
        self.E = torch.nn.Embedding(num_entities, d)
        self.R = torch.nn.Embedding(num_relations, d)
        self.W = torch.nn.Parameter(torch.randn(d, d, d) * 0.1)
        
        torch.nn.init.xavier_normal_(self.E.weight.data)
        torch.nn.init.xavier_normal_(self.R.weight.data)

model = DummyTuckER(len(entity_rows), len(relation_rows))
torch.save({
    'E_weight': model.E.weight.data,
    'R_weight': model.R.weight.data,
    'W': model.W.data,
    'num_entities': len(entity_rows),
    'num_relations': len(relation_rows),
}, 'monotaro/KG_tail_prediction/model/TuckER_model.pkl')

# ============================================================
# 完了
# ============================================================

print("\n" + "=" * 60)
print(" MonotaRO KG Assets Generation Complete!")
print("=" * 60)
print(f" Entities:  {len(entity_rows)} (all with unique descriptions)")
print(f" Relations: {len(relation_rows)} (15 generic + {len(relation_rows)-15} category-specific)")
print(f" Categories: {len(category_table)}")
print("=" * 60)
print(" Generated files:")
print("   - Entity_linking/product_to_entity_examples.csv")
print("   - E&R/entity_examples.csv")
print("   - E&R/relation_examples.csv")
print("   - relations_for_different_category/category_table.pickle")
print("   - relations_for_different_category/category_refined_rel_new.pkl")
print("   - model/TuckER_model.pkl")
print("=" * 60)

import csv
