import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_messages(df, n_clusters=3):
    """
    Groups messages into topic clusters using TF-IDF + K-Means.
    Adds a 'cluster' column to the DataFrame and returns top keywords per cluster.
    """

    messages = df["message"].astype(str)

    # Convert messages into numeric vectors based on word importance
    # stop_words removes common filler words (is, the, a, etc.)
    vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
    X = vectorizer.fit_transform(messages)

    # Run K-Means to group similar messages together
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X)

    # Find top keywords per cluster (to label what each cluster is "about")
    feature_names = vectorizer.get_feature_names_out()
    cluster_keywords = {}

    for i in range(n_clusters):
        # Get the center point of this cluster
        center = kmeans.cluster_centers_[i]
        # Get indices of the highest-weighted words in this cluster's center
        top_indices = center.argsort()[-5:][::-1]
        top_words = [feature_names[idx] for idx in top_indices]
        cluster_keywords[i] = top_words

    return df, cluster_keywords


if __name__ == "__main__":
    df = pd.read_csv("../data/parsed_chat.csv")

    df, keywords = cluster_messages(df, n_clusters=3)

    print("Top keywords per cluster:\n")
    for cluster_id, words in keywords.items():
        print(f"Cluster {cluster_id}: {', '.join(words)}")

    print("\nSample messages per cluster:\n")
    for cluster_id in keywords:
        sample = df[df["cluster"] == cluster_id]["message"].head(2).tolist()
        print(f"Cluster {cluster_id}: {sample}")

    # Save output so teammates can use clustered data without re-running this
    df.to_csv("../data/clustered_chat.csv", index=False)
    print("\nSaved to data/clustered_chat.csv")