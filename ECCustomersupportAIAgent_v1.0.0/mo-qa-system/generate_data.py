import csv
import json
import os
import re
import glob
from collections import defaultdict

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "reproduce", "data", "train", "data_turn")
OUTPUT_FILE = os.path.join(BASE_DIR, "product_data.json")

# Regex patterns for parameter extraction
PARAM_PATTERNS = {
    "price": [r"(\d{1,3}(?:,\d{3})*円)", r"価格は(.+?)です", r"(\d+)円"],
    "weight": [r"(\d+(?:\.\d+)?(?:g|kg|mg))", r"重さは(.+?)です", r"重量は(.+?)です"],
    "size": [r"(幅.+?奥行.+?)です", r"サイズは(.+?)です", r"寸法は(.+?)です", r"全長は(.+?)です", r"(\d+(?:mm|cm|m))"],
    "material": [r"材質は(.+?)です", r"(.+?)製です"],
    "voltage": [r"(\d+V(?:仕様)?)", r"電圧は(.+?)です"],
    "torque": [r"(\d+(?:\.\d+)?N・m)", r"トルクは(.+?)です"],
    "capacity": [r"(\d+(?:\.\d+)?Ah)", r"容量は(.+?)です"],
    "rpm": [r"(\d+rpm)", r"回転数は(.+?)です"],
    "temp_range": [r"(.+?℃.+?℃)", r"使用温度範囲は(.+?)です"],
    "waterproof": [r"(IP\d+)", r"防水対応"],
    "warranty": [r"(\d+ヶ月保証)", r"保証期間は(.+?)です"],
}

def extract_product_name(keywords_str):
    """Extract product name from keywords string."""
    # Pattern: Q:Product;...
    try:
        parts = keywords_str.split(";")
        for part in parts:
            if part.startswith("Q:"):
                # Clean up "Q:" prefix
                name = part[2:].strip()
                if name:
                    return name
            elif not part.startswith("A:"):
                # Sometimes the first keyword isn't prefixed if splitting went wrong, 
                # but usually the first item is the product.
                # Let's rely on Q: prefix first.
                pass
        
        # Fallback: take the first token
        return parts[0].replace("Q:", "").strip()
    except:
        return "Unknown Product"

def parse_dialogue(sent):
    """Parse dialogue string into QA pairs."""
    # format: Q:xxx|||A:xxx|||Q:xxx...
    pairs = []
    try:
        segments = sent.split("|||")
        current_q = ""
        
        for seg in segments:
            if seg.startswith("Q:"):
                current_q = seg[2:].strip()
            elif seg.startswith("A:"):
                current_a = seg[2:].strip()
                if current_q:
                    pairs.append({"q": current_q, "a": current_a})
                    current_q = "" # Reset
    except Exception as e:
        print(f"Error parsing dialogue: {e}")
    return pairs

def extract_params(qa_list):
    """Extract parameters from QA answers."""
    params = {}
    for qa in qa_list:
        a_text = qa["a"]
        q_text = qa["q"]
        
        # Check against patterns
        for key, patterns in PARAM_PATTERNS.items():
            for pat in patterns:
                match = re.search(pat, a_text)
                if match:
                    # found a param
                    val = match.group(1) if match.groups() else match.group(0)
                    params[key] = val
                    break
    return params

def main():
    print(f"Scanning CSVs in {DATA_DIR}...")
    csv_files = glob.glob(os.path.join(DATA_DIR, "dialogue_*.csv"))
    csv_files.sort() # Ensure dialogue_1 to 50 order roughly
    
    # Structure: { Category: { ProductName: { "cnt": X, "params": {}, "qa": [] } } }
    kb = defaultdict(lambda: defaultdict(lambda: {"cnt": 0, "params": {}, "qa": []}))
    
    count = 0
    for file_path in csv_files:
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Extract fields
                    category = row.get("first_category", "Uncategorized")
                    keywords = row.get("keywords", "")
                    sent = row.get("sent", "")
                    
                    product_name = extract_product_name(keywords)
                    qa_pairs = parse_dialogue(sent)
                    
                    # Store data
                    prod_entry = kb[category][product_name]
                    prod_entry["cnt"] += 1
                    
                    # Merge QA
                    # Avoid duplicates if possible? For now just append.
                    prod_entry["qa"].extend(qa_pairs)
                    
                    # Extract params and merge
                    new_params = extract_params(qa_pairs)
                    for k, v in new_params.items():
                        # If conflict, maybe keep latest or list? 
                        # Let's overwrite for now, assuming "comprehensive" means filling gaps.
                        # If a different value exists, we might want to keep both? 
                        # For simplicity, let's keep the last seen non-empty value.
                        prod_entry["params"][k] = v
                        
                    count += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Processed {len(csv_files)} files, {count} dialogues.")
    
    # Final cleanup (optional) - verify structure
    final_output = {}
    for cat, products in kb.items():
        final_output[cat] = dict(products)
        
    print(f"Saving to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    
    print("Done.")

if __name__ == "__main__":
    main()
