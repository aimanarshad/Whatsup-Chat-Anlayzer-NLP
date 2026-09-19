# ChatPulse

An NLP-based analytics tool that takes an exported WhatsApp chat and automatically extracts:
- Participant activity stats
- Sentiment trends over time
- Word & emoji usage patterns
- Auto-discovered conversation topics (via K-Means clustering)

## Tech Stack
- **Parsing & Data:** Python, Regex, Pandas
- **NLP:** VADER (sentiment), TF-IDF + K-Means (topic clustering), emoji library
- **Backend:** FastAPI
- **Frontend:** Streamlit / Next.js

## Project Structure

chatpulse-nlp-project/
├── data/          # Sample chat exports + generated CSVs
├── parsing/       # Chat parsing script ✅ Done
├── clustering/    # Topic clustering script ✅ Done
├── nlp/           # Sentiment & word/emoji analysis ✅ Done
├── backend/       # FastAPI backend — pending
├── frontend/      # Dashboard — pending
├── docs/          # Step-by-step documentation for each script
└── requirements.txt

## Progress

| Step | Status | Docs |
|---|---|---|
| Chat parsing | ✅ Done | docs/01_parsing.md |
| Topic clustering | ✅ Done | docs/02_clustering.md |
| Sentiment + word/emoji analysis | ✅ Done | docs/03_sentiment_emoji.md |
| Backend (FastAPI) | ⏳ Pending | — |
| Frontend dashboard | ⏳ Pending | — |

## How to run what's done so far

```bash
# 1. Parse the chat
cd parsing
python parser.py

# 2. Cluster into topics
cd ../clustering
python cluster.py

# 3. Run sentiment + word/emoji analysis
cd ../nlp
python sentiment_analysis.py
```

## Team
- **Aiman Arshad** — Parsing, data pipeline, clustering, sentiment & word/emoji analysis
- **[Teammate B]** — Backend (FastAPI)
- **[Teammate C]** — Frontend dashboard