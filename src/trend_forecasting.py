import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_topic(df, topic, days=14):
    d = df[df["topic"] == topic].copy()
    daily = d.groupby("date", as_index=False)["viral_coefficient"].mean().sort_values("date")
    if len(daily) < 10:
        return None
    x = np.arange(len(daily)).reshape(-1,1)
    y = daily["viral_coefficient"].to_numpy()
    model = LinearRegression().fit(x, y)
    future_x = np.arange(len(daily), len(daily)+days).reshape(-1,1)
    pred = model.predict(future_x)
    return pd.DataFrame({"day_ahead": np.arange(1,days+1), "forecast_viral_coefficient": pred})

if __name__ == "__main__":
    df = pd.read_csv("data/content_performance.csv", parse_dates=["date"])
    for topic in df["topic"].unique():
        out = forecast_topic(df, topic)
        if out is not None:
            print(topic, "trend:", round(out["forecast_viral_coefficient"].iloc[-1] - out["forecast_viral_coefficient"].iloc[0], 3))
