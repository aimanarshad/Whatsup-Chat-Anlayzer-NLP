# Step 1: Chat Parsing

## What this does
Converts a raw WhatsApp exported `.txt` chat file into a clean, structured table
with columns: date, time, sender, message, datetime.

## Input
- `data/sample_chat.txt` (or any WhatsApp chat exported as .txt, "Without Media")

## Output
- `data/parsed_chat.csv` — structured chat data, ready for further analysis

## How to run
```bash
cd parsing
python parser.py
```

## Key logic
- Uses regex to detect WhatsApp's line format: `date, time - sender: message`
- Handles multi-line messages (when a message wraps without a new timestamp)
- Combines date + time into a single `datetime` column for time-based analysis later

## What's next / who uses this
- `clustered_chat.csv` (clustering step) builds on top of this file
- Sentiment analysis (Teammate B) will also read `parsed_chat.csv` directly