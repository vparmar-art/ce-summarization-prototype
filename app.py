import streamlit as st
from data_utils import load_threads
from summarizer import summarize_gpt
from workflow_manager import save_approved, load_approved
from impact_metrics import show_impact_panel
import json
import pandas as pd

st.set_page_config(page_title="CE Email Summarization", layout="wide")
st.title("Customer Experience Email Summarization Prototype")

# Load threads
df = load_threads("ce_exercise_threads UPDATED.txt")
st.dataframe(df[["thread_id", "topic", "product"]])

# Session state for summaries
if "summaries" not in st.session_state:
    st.session_state["summaries"] = {}

st.write("### Edit & Approve Summaries")

# Main workflow loop
for i, row in df.iterrows():
    st.subheader(f"{row['thread_id']} — {row['topic']} ({row['product']})")

    if st.button(f"Generate Summary {row['thread_id']}", key=f"gen_{row['thread_id']}"):
        with st.spinner("Summarizing..."):
            summary = summarize_gpt(row["conversation"])
            st.session_state["summaries"][row["thread_id"]] = summary

    if row["thread_id"] in st.session_state["summaries"]:
        summary = st.text_area(
            f"Edit summary {row['thread_id']}",
            st.session_state["summaries"][row["thread_id"]],
            key=f"edit_{row['thread_id']}"
        )
        st.session_state["summaries"][row["thread_id"]] = summary

        if st.button(f"✅ Approve {row['thread_id']}", key=f"approve_{row['thread_id']}"):
            save_approved(row["thread_id"], row["topic"], row["product"], summary)
            st.success(f"Saved {row['thread_id']}")

st.write("---")
st.subheader("📤 Export Approved Summaries")
approved_df = load_approved()

if not approved_df.empty:
    st.dataframe(approved_df[["thread_id", "topic", "product", "approved_summary"]])

    st.write("### Suggested Warehouse Actions")
    for _, row in approved_df.iterrows():
        actions = json.loads(row["suggested_actions"]) if "suggested_actions" in row and pd.notna(row["suggested_actions"]) else []
        st.markdown(f"**{row['thread_id']} — {row['topic']} ({row['product']})**")

        for action in actions:
            if st.button(f"✅ {action}", key=f"{row['thread_id']}_{action}"):
                st.success(f"Action '{action}' marked done for {row['thread_id']}")

        st.write("---")

    st.download_button(
        label="Download Approved Summaries",
        data=approved_df.to_csv(index=False),
        file_name="approved_summaries.csv",
        mime="text/csv",
        key="download_approved_csv"
    )
else:
    st.info("No approved summaries yet.")

# Impact metrics panel
show_impact_panel(df)