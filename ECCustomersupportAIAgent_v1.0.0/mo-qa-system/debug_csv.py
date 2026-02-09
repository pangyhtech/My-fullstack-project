import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "reproduce", "data", "train", "data_turn")
FILE_PATH = os.path.join(DATA_DIR, "dialogue_1.csv")

def main():
    print(f"Reading {FILE_PATH}...")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i > 2: break
            print(f"--- Row {i} ---")
            print(f"Keys: {list(row.keys())}")
            print(f"Sent: '{row.get('sent', 'MISSING')}'")
            print(f"Keywords: '{row.get('keywords', 'MISSING')}'")

if __name__ == "__main__":
    main()
