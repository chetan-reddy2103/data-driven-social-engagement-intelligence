import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

FEATURES = [
    "impressions","likes","comments","shares","saves",
    "retention_rate","video_length_sec","followers_before"
]

def train(path="data/content_performance.csv"):
    df = pd.read_csv(path)
    X = df[FEATURES].fillna(0)
    y = df["viral_label"].map({"Non-Viral":0, "Viral":1})
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.2, random_state=42, stratify=y
    )
    model = RandomForestClassifier(
        n_estimators=250, max_depth=10, min_samples_leaf=4,
        random_state=42, class_weight="balanced"
    )
    model.fit(X_train, y_train)
    p = model.predict_proba(X_test)[:,1]
    print("ROC-AUC:", round(roc_auc_score(y_test, p), 4))
    print(classification_report(y_test, (p >= .5).astype(int)))
    joblib.dump(model, "viral_model.joblib")
    return model

if __name__ == "__main__":
    train()
