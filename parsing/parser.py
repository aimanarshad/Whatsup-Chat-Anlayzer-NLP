import re
import pandas as pd

def parse_chat(file_path):
    """
    Parses a WhatsApp exported .txt chat file into a structured DataFrame
    with columns: date, time, sender, message
    """

    # Pattern matches lines like: 12/08/24, 9:14 pm - Aiman: bhai kal free ho?
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s?[ap]m) - (.*?): (.*)$'

    data = []

    with open(file_path, encoding='utf-8') as f:
        lines = f.readlines()

    current_entry = None

    for line in lines:
        line = line.strip()
        match = re.match(pattern, line, re.IGNORECASE)

        if match:
            # New message found — save it
            date, time, sender, message = match.groups()
            current_entry = {
                "date": date,
                "time": time,
                "sender": sender,
                "message": message
            }
            data.append(current_entry)
        else:
            # This line is a continuation of the previous message (multi-line text)
            if current_entry and line:
                current_entry["message"] += " " + line

    df = pd.DataFrame(data)

    # Combine date+time into one proper datetime column for later analysis
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], 
                                      format="%d/%m/%y %I:%M %p", 
                                      errors="coerce")

    return df


if __name__ == "__main__":
    df = parse_chat("../data/sample_chat.txt")
    print(df.head(10))
    print(f"\nTotal messages parsed: {len(df)}")
    
    # Save output so teammates/other scripts can use it without re-parsing
    df.to_csv("../data/parsed_chat.csv", index=False)
    print("Saved to data/parsed_chat.csv")