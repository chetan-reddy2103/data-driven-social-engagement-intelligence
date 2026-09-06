import pandas as pd
from scipy.stats import ttest_ind

def run_ab_test(df, variant_col, metric_col):
    a = df[df[variant_col] == df[variant_col].unique()[0]][metric_col].dropna()
    b = df[df[variant_col] == df[variant_col].unique()[1]][metric_col].dropna()
    stat, p = ttest_ind(a, b, equal_var=False)
    return {
        "variant_a": df[variant_col].unique()[0],
        "variant_b": df[variant_col].unique()[1],
        "mean_a": float(a.mean()),
        "mean_b": float(b.mean()),
        "lift_pct": float((b.mean()-a.mean())/a.mean()*100),
        "p_value": float(p),
        "significant": bool(p < .05)
    }

if __name__ == "__main__":
    df = pd.read_csv("data/content_performance.csv")
    print(run_ab_test(df, "format", "engagement_rate_pct"))
    print(run_ab_test(df, "hook", "engagement_rate_pct"))
