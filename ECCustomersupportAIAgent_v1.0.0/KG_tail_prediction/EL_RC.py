# -*- coding: utf-8 -*-
"""
Monotaro版 EL_RC.py (実体リンク + 関係分類)
Input: Third Category (商品カテゴリ)
Output: Linked entities(List), Related relations(List)

MonotaRO 24カテゴリ対応版
"""

import pickle
import pandas as pd

# 日本語分類のため jieba 不要、MeCab も不要 (単純マッチング)

def relations_compare(first_category: str) -> int:
    """
    カテゴリテキストから一級分類IDを取得
    MonotaRO 24カテゴリ対応
    """
    category_dict = {
        1: "安全保護具・作業服・安全靴",
        2: "物流/保管/梱包用品/テープ",
        3: "安全用品/防災・防犯用品/安全標識",
        4: "オフィスサプライ",
        5: "オフィス家具/照明/清掃用品",
        6: "切削工具・研磨材",
        7: "測定・測量用品",
        8: "作業工具/電動・空圧工具",
        9: "スプレー・オイル・グリス/塗料/接着・補修/溶接",
        10: "配管・水廻り部材/ポンプ/空圧・油圧機器・ホース",
        11: "メカニカル部品/機構部品",
        12: "制御機器/はんだ・静電気対策用品",
        13: "建築金物・建材・塗装内装用品",
        14: "空調・電設資材/電気材料",
        15: "ねじ・ボルト・釘/素材",
        16: "自動車用品",
        17: "トラック用品",
        18: "バイク用品",
        19: "自転車用品",
        20: "科学研究・開発用品/クリーンルーム用品",
        21: "厨房機器・キッチン/店舗用品",
        22: "農業資材・園芸用品",
        23: "医療・介護用品",
        24: "その他"
    }
    
    # キーワードマッチング (部分一致)
    first_category_str = str(first_category)
    for key, value in category_dict.items():
        # 分類名の一部がマッチすればOK
        keywords = value.replace('/', '').replace('・', '').split()
        for kw in [value] + keywords:
            if kw in first_category_str or first_category_str in kw:
                return key
    
    return 24  # その他

def get_linked_entities(linking_table: pd.DataFrame, third_category_text: str) -> list:
    """
    商品カテゴリからリンクされたエンティティを取得
    """
    ent_index = []
    is_found = 0
    
    tab_len = linking_table.shape[0]
    
    for i in range(0, tab_len):
        topic = str(linking_table.iloc[i, 0])
        if topic.strip() == str(third_category_text).strip():
            is_found = 1
            break
    
    if not is_found:
        return None
    
    for j in range(1, 20):
        if pd.isnull(linking_table.iloc[i, j]):
            break
        if "ent_" in str(linking_table.iloc[i, j]):
            ent_index.append(linking_table.iloc[i, j])
    
    ent_index = list(set(ent_index))
    return ent_index

def get_related_relations(relation_table: dict, category_table: dict, third_category_text: str) -> list:
    """
    カテゴリに関連する関係を取得
    """
    if third_category_text in category_table.keys():
        first_cate_text = category_table[third_category_text][0]
        rel_judge = relations_compare(first_cate_text)
    else:
        return relation_table.get(24, [])  # その他

    common_relations = relation_table.get(24, [])
    specific_relations = relation_table.get(rel_judge, [])
    return list(set(specific_relations + common_relations))

def EL_RC(third_category: str) -> tuple:
    """
    メイン関数: エンティティリンク + 関係分類
    
    MonotaRO カテゴリ:
    1-安全保護具・作業服・安全靴、2-物流/保管/梱包用品/テープ、3-安全用品/防災・防犯用品/安全標識、
    4-オフィスサプライ、5-オフィス家具/照明/清掃用品、6-切削工具・研磨材、7-測定・測量用品、
    8-作業工具/電動・空圧工具、9-スプレー・オイル・グリス/塗料/接着・補修/溶接、
    10-配管・水廻り部材/ポンプ/空圧・油圧機器・ホース、11-メカニカル部品/機構部品、
    12-制御機器/はんだ・静電気対策用品、13-建築金物・建材・塗装内装用品、14-空調・電設資材/電気材料、
    15-ねじ・ボルト・釘/素材、16-自動車用品、17-トラック用品、18-バイク用品、19-自転車用品、
    20-科学研究・開発用品/クリーンルーム用品、21-厨房機器・キッチン/店舗用品、22-農業資材・園芸用品、
    23-医療・介護用品、24-その他
    """
    
    # 関係ファイルを読み込み
    try:
        with open('monotaro/KG_tail_prediction/data/relations_for_different_category/category_refined_rel_new.pkl', 'rb') as file:
            rel_index = pickle.load(file)
    except FileNotFoundError:
        print("Warning: Relations file not found, using empty dict")
        rel_index = {i: [] for i in range(1, 25)}
    
    # 商品分類ファイルを読み込み
    try:
        with open('monotaro/KG_tail_prediction/data/relations_for_different_category/category_table.pickle', 'rb') as file:
            category_table = pickle.load(file)
    except FileNotFoundError:
        print("Warning: Category table not found, using empty dict")
        category_table = {}
    
    # エンティティリンクファイルを読み込み
    try:
        linking_table = pd.read_csv('monotaro/KG_tail_prediction/data/Entity_linking/product_to_entity_examples.csv', header=None)
    except FileNotFoundError:
        print("Warning: Linking table not found")
        return None, None
    
    linked_entities = get_linked_entities(linking_table, third_category)
    related_relations = get_related_relations(rel_index, category_table, third_category)
    
    if linked_entities is None:
        print(f"エンティティが見つかりません: {third_category}")
        return None, None
    
    return linked_entities, related_relations


if __name__ == "__main__":
    # テスト
    test_categories = ["ヘルメット", "安全靴", "ドリルビット"]
    for cat in test_categories:
        entities, relations = EL_RC(cat)
        print(f"Category: {cat}")
        print(f"  Entities: {entities}")
        print(f"  Relations: {relations}")
