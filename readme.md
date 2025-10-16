# 📧 CE Summarization Prototype

A working prototype that summarizes **multi-threaded Customer Experience (CE) emails** using NLP, provides a **human-in-the-loop approval workflow**, and suggests **next best actions** for associates.  
It also includes **impact analysis (time, cost, CSAT)** to show measurable business outcomes.

---

## 🚀 Features

- **Data ingestion**: Load raw CE email threads from JSON.  
- **NLP Summarization**: GPT-powered summarization of entire threads into 2–3 concise sentences.  
- **Edit + Approve workflow**: Associates can review, edit, and approve AI summaries.  
- **Suggested Actions**: Automatically generates actionable steps (e.g., “Request photos”, “Initiate refund”).  
- **Action Buttons**: Dummy workflow buttons (mark actions as done).  
- **Export**: Save approved summaries + actions to `approved_summaries.csv`.  
- **Impact Metrics**: Compute average thread length, summary compression ratio, and estimate time/cost/CSAT improvements.  
- **Compact UI**: Built in Streamlit for quick prototyping and clean user experience.  

---

## 🛠️ Stack

- **[Streamlit](https://streamlit.io/)** — simple, browser-based UI for prototypes.  
- **[OpenAI GPT (gpt-4o-mini)](https://platform.openai.com/)** — summarization & action generation.  
- **[pandas](https://pandas.pydata.org/)** — data wrangling.  
- **[Altair](https://altair-viz.github.io/)** — charts for impact analysis.  
- **[TextBlob](https://textblob.readthedocs.io/)** *(optional)* — for sentiment analysis if extended.  

---

## 📂 Project Structure
ce_summarization/
 ├── app.py                # Streamlit app orchestrator
 ├── data_utils.py         # Load & preprocess CE threads
 ├── summarizer.py         # Summarization + action generation
 ├── workflow_manager.py   # Approvals, CSV persistence
 ├── impact_metrics.py     # Time/cost/CSAT impact analysis
 ├── requirements.txt      # Python dependencies
 └── ce_exercise_threads UPDATED.txt  # Provided dataset

---

## ⚡️ Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/vparmar-art/ce-summarization-prototype.git
cd ce-summarization-prototype


python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


pip install -r requirements.txt

streamlit run app.py