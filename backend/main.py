import os
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from parsing.parser import parse_chat
from clustering.cluster import cluster_messages
from nlp.sentiment_analysis import (
    analyze_sentiment,
    get_word_frequency,
    get_emoji_frequency,
)

app = FastAPI(title="ChatPulse API")

# Lets the frontend (Next.js / Streamlit / any origin) call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ChatPulse API is running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), n_clusters: int = 3):
    """
    Upload a WhatsApp .txt export and get back the full analysis as JSON.
    """
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Please upload a WhatsApp .txt export")

    # Save upload to a temp file because parse_chat() reads from a file path
    content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        df = parse_chat(tmp_path)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not parse this file. Is it a WhatsApp export?")
    finally:
        os.remove(tmp_path)

    # Clean: drop rows with bad timestamps and media placeholders
    df = df.dropna(subset=["datetime"])
    df = df[~df["message"].str.contains("Media omitted", case=False, na=False)]
    df = df.reset_index(drop=True)

    if df.empty:
        raise HTTPException(status_code=400, detail="No messages found in this file")

    # ---------- 1. Activity ----------
    per_sender = df["sender"].value_counts()
    per_hour = df["datetime"].dt.hour.value_counts().sort_index()
    activity = {
        "total_messages": int(len(df)),
        "most_active_sender": str(per_sender.idxmax()),
        "messages_per_sender": {str(k): int(v) for k, v in per_sender.items()},
        "messages_per_hour": {int(k): int(v) for k, v in per_hour.items()},
    }

    # ---------- 2. Sentiment ----------
    df = analyze_sentiment(df)
    overall = df["sentiment_label"].value_counts()
    by_sender = df.groupby("sender")["sentiment_score"].mean().round(3)
    over_time = df.groupby(df["datetime"].dt.date.astype(str))["sentiment_score"].mean().round(3)
    sentiment = {
        "overall": {str(k): int(v) for k, v in overall.items()},
        "average_by_sender": {str(k): float(v) for k, v in by_sender.items()},
        "over_time": {str(k): float(v) for k, v in over_time.items()},
    }

    # ---------- 3. Words and emojis ----------
    words = {
        sender: [{"word": w, "count": c} for w, c in lst]
        for sender, lst in get_word_frequency(df).items()
    }
    emojis = {
        sender: [{"emoji": e, "count": c} for e, c in lst]
        for sender, lst in get_emoji_frequency(df).items()
    }

    # ---------- 4. Clustering (topics) ----------
    clusters = []
    try:
        k = max(1, min(n_clusters, len(df)))
        df, keywords = cluster_messages(df, n_clusters=k)
        for cid, top_words in keywords.items():
            subset = df[df["cluster"] == cid]
            clusters.append({
                "cluster_id": int(cid),
                "keywords": top_words,
                "message_count": int(len(subset)),
                "sample_messages": subset["message"].head(3).tolist(),
            })
    except ValueError:
        # e.g. chat too short or only filler words, so there is nothing to cluster
        clusters = []

    return {
        "activity": activity,
        "sentiment": sentiment,
        "top_words": words,
        "top_emojis": emojis,
        "topic_clusters": clusters,
    }