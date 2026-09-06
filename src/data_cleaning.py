import pandas as pd
import numpy as np

def clean_content(path="data/content_performance.csv"):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    numeric = ["impressions","likes","comments","shares","saves","retention_rate","followers_gained"]
    for c in numeric:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    df = df.drop_duplicates(subset=["content_id"])
    df["engagement_rate_pct"] = ((df["likes"]+df["comments"]+df["shares"]+df["saves"]) / df["impressions"].replace(0,np.nan)*100).fillna(0)
    df["save_to_share_ratio"] = (df["saves"]/df["shares"].replace(0,np.nan)).fillna(0)
    df["viral_coefficient"] = ((df["shares"]*3+df["saves"]*2+df["comments"]*1.5+df["likes"]*.5)/df["impressions"].replace(0,np.nan)*100).fillna(0)
    return df

if __name__ == "__main__":
    df = clean_content()
    df.to_csv("data/content_performance_clean.csv", index=False)
    print(f"Cleaned {len(df):,} content records.")
