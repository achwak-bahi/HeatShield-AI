"""
HeatShield AI - Entraînement des modèles ML
Objectif: prédire high_risk_binary (0/1) à partir des features météo.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "algeria_weather_features_v1.csv"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

TARGET = "high_risk_binary"


def load_data():
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])
    return df


def select_features(df):
    candidate_features = [
        "temp_max", "temp_min", "temp_mean", "humidity", "wind_max", "rain",
        "et0", "vpd_max", "radiation",
        "heat_humidity_ratio", "wind_drought_index", "dry_air_index", "rain_protection",
        "temp_3d_avg", "temp_7d_avg",
        "humidity_3d_avg", "humidity_7d_avg",
        "wind_3d_avg", "wind_7d_avg",
        "rain_3d_sum", "rain_7d_sum",
        "et0_7d_sum", "vpd_7d_avg",
        "hot_day_38", "hot_day_40", "hot_day_42",
        "hot_days_38_rolling", "hot_days_40_rolling",
        "cumulative_heat_stress", "heatwave_intensity",
        "consecutive_hot_days_38",
    ]

    features = [c for c in candidate_features if c in df.columns]
    X = df[features].copy()
    y = df[TARGET].copy()

    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)

    return X, y, features


def split_data(X, y):
    return train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )


def get_models():
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            random_state=42,
            n_jobs=-1
        ),
        "XGBoost": XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42,
            eval_metric="logloss"
        ),
        "LightGBM": LGBMClassifier(
            n_estimators=200,
            learning_rate=0.05,
            random_state=42
        ),
    }
    return models


def evaluate_model(name, model, X_train, X_test, y_train, y_test, scale=False):
    scaler = None

    if scale:
        scaler = StandardScaler()
        X_train_used = scaler.fit_transform(X_train)
        X_test_used = scaler.transform(X_test)
    else:
        X_train_used = X_train
        X_test_used = X_test

    model.fit(X_train_used, y_train)
    y_pred = model.predict(X_test_used)

    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test_used)[:, 1]
    else:
        y_proba = y_pred

    metrics = {
        "model": name,
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }

    print("\n" + "=" * 60)
    print(f"Modèle: {name}")
    print("=" * 60)
    print(classification_report(y_test, y_pred, zero_division=0))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model, scaler, metrics


def save_best_model(best_name, best_model, scaler, features):
    joblib.dump(best_model, MODEL_DIR / "best_model.pkl")
    joblib.dump(features, MODEL_DIR / "feature_names.pkl")

    if scaler is not None:
        joblib.dump(scaler, MODEL_DIR / "scaler.pkl")

    with open(MODEL_DIR / "best_model_name.txt", "w", encoding="utf-8") as f:
        f.write(best_name)

    print(f"\n✅ Meilleur modèle sauvegardé: {best_name}")


def main():
    print("=" * 60)
    print("🔥 HeatShield AI — Entraînement ML")
    print("=" * 60)

    df = load_data()
    X, y, features = select_features(df)

    print(f"Dataset shape: {df.shape}")
    print(f"Nombre de features: {len(features)}")
    print(f"Target balance:\n{y.value_counts(normalize=True)}")

    X_train, X_test, y_train, y_test = split_data(X, y)

    models = get_models()
    results = []

    trained = {}

    for name, model in models.items():
        scale = name == "Logistic Regression"
        trained_model, scaler, metrics = evaluate_model(
            name, model, X_train, X_test, y_train, y_test, scale=scale
        )
        results.append(metrics)
        trained[name] = (trained_model, scaler)

    results_df = pd.DataFrame(results).sort_values(by="f1", ascending=False)

    print("\n" + "=" * 60)
    print("Résumé des performances:")
    print(results_df)

    results_df.to_csv(PROJECT_ROOT / "data" / "processed" / "model_results.csv", index=False)

    best_name = results_df.iloc[0]["model"]
    best_model, best_scaler = trained[best_name]
    save_best_model(best_name, best_model, best_scaler, features)

    print("=" * 60)


if __name__ == "__main__":
    main()