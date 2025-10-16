import json
import pandas as pd

def load_threads(path):
    """Load CE threads from JSON file."""
    with open(path) as f:
        data = json.load(f)

    threads = []
    for t in data["threads"]:
        text = " ".join([m["body"] for m in t["messages"]])
        threads.append({
            "thread_id": t["thread_id"],
            "topic": t["topic"],
            "product": t["product"],
            "conversation": text
        })

    return pd.DataFrame(threads)