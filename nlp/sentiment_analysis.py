import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
import emoji
import re

def analyze_sentiment(df):
    """
    Adds sentiment score and label (Positive/Negative/Neutral) for each message.
    """
    analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(text):
        score = analyzer.polarity_scores(str(text))["compound"]
        if score >= 0.05:
            label = "Positive"
        elif score <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"
        return pd.Series([score, label])

    df[["sentiment_score", "sentiment_label"]] = df["message"].apply(get_sentiment)
    return df


def get_word_frequency(df, top_n=10):
    """
    Returns the most common words per sender (ignoring very short/common words).
    """
    stopwords = {"the","is","a","to","and","of","in","it","i","you","for","on","this","that","hai","ka","ke","ki","ko","se","hi","bhi"}
    
    word_freq_by_sender = {}

    for sender in df["sender"].unique():
        sender_messages = df[df["sender"] == sender]["message"].str.lower()
        words = []
        for msg in sender_messages:
            words.extend(re.findall(r'\b[a-zA-Z]+\b', msg))
        words = [w for w in words if w not in stopwords and len(w) > 2]
        word_freq_by_sender[sender] = Counter(words).most_common(top_n)

    return word_freq_by_sender


def get_emoji_frequency(df):
    """
    Returns the most used emojis per sender.
    """
    emoji_freq_by_sender = {}

    for sender in df["sender"].unique():
        sender_messages = df[df["sender"] == sender]["message"]
        all_emojis = []
        for msg in sender_messages:
            all_emojis.extend([c for c in str(msg) if c in emoji.EMOJI_DATA])
        emoji_freq_by_sender[sender] = Counter(all_emojis).most_common(5)

    return emoji_freq_by_sender


if __name__ == "__main__":
    df = pd.read_csv("../data/parsed_chat.csv")

    # Sentiment
    df = analyze_sentiment(df)
    print("Sentiment sample:\n", df[["sender", "message", "sentiment_label"]].head(10))

    # Word frequency
    word_freq = get_word_frequency(df)
    print("\nTop words per sender:")
    for sender, words in word_freq.items():
        print(f"{sender}: {words}")

    # Emoji frequency
    emoji_freq = get_emoji_frequency(df)
    print("\nTop emojis per sender:")
    for sender, emojis in emoji_freq.items():
        print(f"{sender}: {emojis}")

    # Save output
    df.to_csv("../data/sentiment_chat.csv", index=False)
    print("\nSaved to data/sentiment_chat.csv")