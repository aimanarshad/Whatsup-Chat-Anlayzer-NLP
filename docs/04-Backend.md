# Step 4: Backend API (FastAPI)

## What this does
Exposes the whole ChatPulse analysis pipeline as one API endpoint.
The frontend uploads a WhatsApp .txt export and receives all results as JSON.

## Endpoints
- `GET /` : health check
- `POST /analyze` : upload a chat file, get full analysis
  - Form field: `file` (the .txt export)
  - Optional query param: `n_clusters` (default 3)

## Pipeline inside /analyze
1. Save upload to a temp file and parse it (`parsing/parser.py`)
2. Clean: drop bad timestamps and "Media omitted" rows
3. Activity stats: messages per sender, per hour
4. Sentiment: VADER scores, overall counts, average per sender, trend by date
5. Word and emoji frequency per sender
6. Topic clustering with TF-IDF + K-Means (`clustering/cluster.py`)

## Response format
```json
{
  "activity": { "total_messages", "most_active_sender", "messages_per_sender", "messages_per_hour" },
  "sentiment": { "overall", "average_by_sender", "over_time" },
  "top_words": { "<sender>": [ {"word", "count"} ] },
  "top_emojis": { "<sender>": [ {"emoji", "count"} ] },
  "topic_clusters": [ {"cluster_id", "keywords", "message_count", "sample_messages"} ]
}
```

## How to run
From the repo root (not inside backend/):
```bash
python -m uvicorn backend.main:app --reload
```
Test page: http://127.0.0.1:8000/docs

## Notes
- Each of parsing/, clustering/, nlp/, backend/ needs an empty `__init__.py`
- CORS is open so any frontend can call the API
- Parser currently supports the Android export format

## What's next / who uses this
- Frontend: call POST /analyze and build one chart or card per JSON section