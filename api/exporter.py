import pandas as pd

def export_to_excel(records, path="chat_history.xlsx"):
    df = pd.DataFrame(records)
    df.to_excel(path, index=False)

def export_to_json(records, path="chat_history.json"):
    import json
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)
