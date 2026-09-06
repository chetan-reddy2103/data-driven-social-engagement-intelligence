import re
import pandas as pd

RELATABLE_PATTERNS = [
    r"\b(i thought i was the only one|same|me too|exactly|relatable|needed this|"
    r"understood|put.*into words|struggling with the same|described my situation)\b"
]

def classify_comment(text):
    text = str(text).lower()
    score = sum(bool(re.search(p, text)) for p in RELATABLE_PATTERNS)
    return "Relatable" if score else "Neutral"

def analyze(path="data/user_comments.csv"):
    df = pd.read_csv(path)
    df["nlp_label"] = df["comment_text"].apply(classify_comment)
    return df

if __name__ == "__main__":
    df = analyze()
    df.to_csv("data/comments_analyzed.csv", index=False)
    print(df["nlp_label"].value_counts())
