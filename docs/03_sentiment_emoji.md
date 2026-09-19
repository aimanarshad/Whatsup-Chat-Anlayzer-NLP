# Step 3: Sentiment Analysis + Word/Emoji Frequency

## What this does
Adds sentiment scoring to every message, and calculates the most-used words
and emojis per sender.

## Input
- `data/parsed_chat.csv` (output of parsing step)

## Output
- `data/sentiment_chat.csv` — parsed data + sentiment_score + sentiment_label columns
- Printed: top words per sender, top emojis per sender

## How to run
```bash
cd nlp
python sentiment_analysis.py
```

## Key logic
- VADER (pretrained sentiment tool) scores each message from -1 to +1
- Score is converted into a label: Positive (>=0.05), Negative (<=-0.05), Neutral (in between)
- Word frequency filters out common English + Roman Urdu filler words before counting
- Emoji frequency scans each message character-by-character using the `emoji` library

## Notes
- No model training needed — VADER is pretrained and ready to use
- Stopword list can be expanded later if real chat data has more filler words

## What's next / who uses this
- Backend (Teammate C) exposes sentiment trend + word/emoji stats via API endpoints
- Frontend (Teammate C) plots sentiment over time and displays word/emoji charts