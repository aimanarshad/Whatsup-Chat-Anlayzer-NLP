# Step 2: Topic Clustering

## What this does
Groups chat messages into topic clusters automatically using TF-IDF + K-Means,
without manually defining any topics. Satisfies the course's clustering requirement.

## Input
- `data/parsed_chat.csv` (output of parsing step)

## Output
- `data/clustered_chat.csv` — same data as before, plus a new `cluster` column
- Printed top keywords per cluster (used to label what each cluster is about)

## How to run
```bash
cd clustering
python cluster.py
```

## Key logic
- TF-IDF converts each message into a numeric vector based on important words
- K-Means groups similar message-vectors into `n_clusters` groups (default: 3)
- Top keywords per cluster are extracted manually since K-Means doesn't name clusters

## Notes
- Cluster quality improves significantly with more real messages (sample data is small)
- `n_clusters` can be increased once real chat data is used, depending on topic variety

## What's next / who uses this
- Backend (Teammate C) will expose this clustered data via an API endpoint
- Frontend (Teammate C) will display cluster labels/keywords on the dashboard