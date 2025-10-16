import pandas as pd
import altair as alt
import streamlit as st
from workflow_manager import load_approved

def compute_metrics(df, approved_df):
    """Compute metrics (lengths, compression ratio) using approved summaries only."""
    merged = df.merge(approved_df, on="thread_id", how="inner")
    metrics = []
    for _, row in merged.iterrows():
        orig_len = len(row["conversation"].split())
        sum_len = len(str(row["approved_summary"]).split())
        metrics.append({
            "thread_id": row["thread_id"],
            "orig_len": orig_len,
            "sum_len": sum_len,
            "compression_ratio": sum_len / orig_len if orig_len > 0 else 0
        })
    return pd.DataFrame(metrics)

def show_impact_panel(df, threads_per_day=500, agent_cost_per_hour=300):
    st.write("---")
    st.subheader("📊 Operational Impact Estimate")

    approved_df = load_approved()
    if approved_df.empty:
        st.info("Approve some summaries to see impact metrics.")
        return

    metrics_df = compute_metrics(df, approved_df)

    if metrics_df.empty:
        st.info("No overlap between dataset and approved summaries yet.")
        return

    avg_orig = metrics_df["orig_len"].mean()
    avg_sum = metrics_df["sum_len"].mean()
    avg_ratio = metrics_df["compression_ratio"].mean()

    # Assume reading speed ~160 words/minute
    manual_time = avg_orig / 160
    ai_time = avg_sum / 160
    time_saved_per_thread = manual_time - ai_time

    time_saved_total = time_saved_per_thread * threads_per_day
    hours_saved_total = time_saved_total / 60
    cost_saved = hours_saved_total * agent_cost_per_hour

    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Thread Length", f"{avg_orig:.0f} words")
    col2.metric("Avg Summary Length", f"{avg_sum:.0f} words")
    col3.metric("Compression Ratio", f"{avg_ratio*100:.1f}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("Time Saved / Thread", f"{time_saved_per_thread:.2f} min")
    col5.metric("⏱ Time Saved / Day", f"{time_saved_total:.0f} min (~{hours_saved_total:.1f} hrs)")
    col6.metric("💰 Cost Saved / Day", f"₹{cost_saved:,.0f}")

    # Visualization: original vs summary length
    impact_data = pd.DataFrame({
        'Type': ['Original', 'Summary'],
        'Words': [avg_orig, avg_sum]
    })

    chart = alt.Chart(impact_data).mark_bar().encode(
        x='Type',
        y='Words',
        color='Type'
    ).properties(width=400, height=300)

    st.altair_chart(chart, use_container_width=True)