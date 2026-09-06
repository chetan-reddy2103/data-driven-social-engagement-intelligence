from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Resolve project paths from app.py so the dashboard works reliably on
# Streamlit Cloud regardless of the current working directory.
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

st.set_page_config(page_title="Social Engagement Intelligence", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    content = pd.read_csv(DATA_DIR / "content_performance.csv", parse_dates=["date"])
    comments = pd.read_csv(DATA_DIR / "comments_analyzed.csv", parse_dates=["created_at"])
    ab = pd.read_csv(DATA_DIR / "ab_test_results.csv")
    forecast = pd.read_csv(DATA_DIR / "topic_forecast_14d.csv")
    return content, comments, ab, forecast

df, comments, ab, forecast = load_data()

st.title("📊 Data-Driven Social Engagement Intelligence")
st.caption("Growth • Relatability • Virality • A/B Testing • Recommendations • Trend Forecasting")

# Sidebar
st.sidebar.header("Filters")
platforms = st.sidebar.multiselect("Platform", sorted(df["platform"].unique()), default=list(df["platform"].unique()))
topics = st.sidebar.multiselect("Topic", sorted(df["topic"].unique()), default=list(df["topic"].unique()))
filtered = df[df["platform"].isin(platforms) & df["topic"].isin(topics)].copy()

# KPI row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Posts", f"{len(filtered):,}")
c2.metric("Avg Engagement", f"{filtered['engagement_rate_pct'].mean():.2f}%")
c3.metric("Avg Viral Coefficient", f"{filtered['viral_coefficient'].mean():.3f}")
c4.metric("Followers Gained", f"{filtered['followers_gained'].sum():,}")

st.divider()

# Growth + virality
left, right = st.columns(2)
with left:
    topic_perf = filtered.groupby("topic", as_index=False).agg(
        viral=("viral_coefficient", "mean")
    ).sort_values("viral", ascending=False)
    fig = px.bar(topic_perf, x="topic", y="viral", title="Viral Coefficient by Topic")
    fig.update_layout(xaxis_title="Topic", yaxis_title="Average Viral Coefficient")
    st.plotly_chart(fig, use_container_width=True)

with right:
    monthly = filtered.assign(month=filtered["date"].dt.to_period("M").astype(str)).groupby(
        "month", as_index=False
    ).agg(followers=("followers_gained", "sum"))
    fig = px.line(monthly, x="month", y="followers", markers=True, title="Follower Growth Trend")
    st.plotly_chart(fig, use_container_width=True)

# Engagement signals
left, right = st.columns(2)
with left:
    fig = px.scatter(
        filtered.sample(min(1500, len(filtered)), random_state=42),
        x="shares", y="saves", size="impressions", color="topic",
        hover_data=["content_id", "viral_coefficient"],
        title="Shares vs Saves"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.box(
        filtered, x="format", y="engagement_rate_pct", color="hook",
        title="A/B View: Format and Hook"
    )
    st.plotly_chart(fig, use_container_width=True)

# Statistical A/B results
st.subheader("🧪 Statistical A/B Test Results")
ab_display = ab.copy()
ab_display["p_value"] = ab_display["p_value"].map(lambda x: f"{x:.6g}")
ab_display["lift_variant_b_pct"] = ab_display["lift_variant_b_pct"].map(lambda x: f"{x:+.2f}%")
st.dataframe(ab_display, use_container_width=True, hide_index=True)

# NLP section
st.subheader("💬 Audience Relatability / NLP Analysis")
nlp_counts = comments["nlp_label"].value_counts().rename_axis("label").reset_index(name="comments")
nlp_left, nlp_right = st.columns(2)
with nlp_left:
    fig = px.pie(nlp_counts, names="label", values="comments", title="Relatable vs Neutral Comments")
    st.plotly_chart(fig, use_container_width=True)
with nlp_right:
    relatable_ids = comments.loc[comments["nlp_label"] == "Relatable", "content_id"]
    nlp_topic = filtered[filtered["content_id"].isin(relatable_ids)].groupby("topic", as_index=False).size()
    nlp_topic.columns = ["topic", "relatable_comments"]
    nlp_topic = nlp_topic.sort_values("relatable_comments", ascending=False)
    fig = px.bar(nlp_topic, x="topic", y="relatable_comments", title="Relatable Comments by Topic")
    st.plotly_chart(fig, use_container_width=True)

# Forecasting
st.subheader("📈 14-Day Viral Trend Forecast")
forecast_filtered = forecast[forecast["topic"].isin(topics)]
fig = px.line(
    forecast_filtered, x="day_ahead", y="forecast_viral_coefficient",
    color="topic", markers=True,
    title="Forecasted Viral Coefficient by Topic"
)
fig.update_layout(xaxis_title="Days Ahead", yaxis_title="Forecast Viral Coefficient")
st.plotly_chart(fig, use_container_width=True)

# Top posts
st.subheader("🏆 Top 15 Viral Posts")
cols = ["content_id", "topic", "platform", "format", "hook", "shares", "saves", "retention_rate", "viral_coefficient"]
st.dataframe(
    filtered.sort_values("viral_coefficient", ascending=False)[cols].head(15),
    use_container_width=True, hide_index=True
)

# Recommendations
st.subheader("💡 Prescriptive Recommendations")
group = filtered.groupby(["topic", "format", "caption_style"], as_index=False).agg(
    engagement=("engagement_rate_pct", "mean"),
    viral=("viral_coefficient", "mean"),
    retention=("retention_rate", "mean"),
    posts=("content_id", "count")
)
group["score"] = group["engagement"] * .45 + group["viral"] * 10 * .35 + group["retention"] * 100 * .20
st.dataframe(
    group.sort_values("score", ascending=False).head(10),
    use_container_width=True, hide_index=True
)

st.subheader("📝 Project Content Series")
st.markdown("See `reports/content_series.md` for the 10 creative concepts used as the test subject.")

st.info(
    "Demo note: the included dataset is synthetic and reproducible. "
    "For production deployment, replace the CSV ingestion layer with authenticated platform API/export data."
)
