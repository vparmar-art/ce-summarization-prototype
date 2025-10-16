import pandas as pd
import os, json
from summarizer import suggest_actions   # import action generator

CSV_PATH = "approved_summaries.csv"

def save_approved(thread_id, topic, product, summary):
    actions = suggest_actions(summary)
    df = pd.DataFrame([{
        "thread_id": thread_id,
        "topic": topic,
        "product": product,
        "approved_summary": summary,
        "suggested_actions": json.dumps(actions)  # store as JSON string
    }])
    write_header = not os.path.exists(CSV_PATH)
    df.to_csv(CSV_PATH, mode="a", header=write_header, index=False)

def load_approved():
    """Load all approved summaries from CSV, return empty DF if not exists."""
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        return pd.DataFrame(columns=[
            "thread_id", "topic", "product", "approved_summary", "suggested_actions"
        ])
    return pd.read_csv(CSV_PATH)