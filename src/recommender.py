import pandas as pd

def recommendations(path="data/content_performance.csv"):
    df = pd.read_csv(path)
    top = df.groupby(["topic","format","caption_style"], as_index=False).agg(
        avg_engagement=("engagement_rate_pct","mean"),
        avg_viral=("viral_coefficient","mean"),
        avg_retention=("retention_rate","mean"),
        posts=("content_id","count")
    )
    top["recommendation_score"] = (
        top["avg_engagement"]*0.45 +
        top["avg_viral"]*0.35 +
        top["avg_retention"]*100*0.20
    )
    return top.sort_values("recommendation_score", ascending=False).head(10)

if __name__ == "__main__":
    print(recommendations().to_string(index=False))
