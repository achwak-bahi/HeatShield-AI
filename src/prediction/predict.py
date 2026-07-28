"""
HeatShield AI - Service de prédiction
Charge le modèle entraîné et prédit le niveau de risque.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "models"

MODEL_FILE = MODEL_DIR / "best_model.pkl"
FEATURES_FILE = MODEL_DIR / "feature_names.pkl"
SCALER_FILE = MODEL_DIR / "scaler.pkl"
BEST_MODEL_NAME_FILE = MODEL_DIR / "best_model_name.txt"


def load_artifacts():
    model = joblib.load(MODEL_FILE)
    features = joblib.load(FEATURES_FILE)

    scaler = None
    if SCALER_FILE.exists():
        scaler = joblib.load(SCALER_FILE)

    model_name = "unknown"
    if BEST_MODEL_NAME_FILE.exists():
        model_name = BEST_MODEL_NAME_FILE.read_text(encoding="utf-8").strip()

    return model, features, scaler, model_name


def risk_probability_to_level(prob):
    """Convertit une probabilité en niveau lisible."""
    score = prob * 100

    if score < 25:
        return "Faible", score
    elif score < 50:
        return "Modéré", score
    elif score < 75:
        return "Élevé", score
    return "Critique", score


def build_features(
    temp_max,
    humidity,
    wind_max,
    rain,
    et0,
    vpd_max,
    radiation,
    temp_min=None,
    temp_mean=None,
    consecutive_hot_days_38=0,
):
    """
    Construit un vecteur de features cohérent avec l'entraînement.
    """

    if temp_min is None:
        temp_min = temp_max - 8
    if temp_mean is None:
        temp_mean = (temp_max + temp_min) / 2

    data = {
        "temp_max": temp_max,
        "temp_min": temp_min,
        "temp_mean": temp_mean,
        "humidity": humidity,
        "wind_max": wind_max,
        "rain": rain,
        "et0": et0,
        "vpd_max": vpd_max,
        "radiation": radiation,
    }

    # Interactions
    data["heat_humidity_ratio"] = temp_max / (humidity + 1)
    data["wind_drought_index"] = wind_max * (et0 + 1)
    data["dry_air_index"] = vpd_max * (1 + (temp_max / 100))
    data["rain_protection"] = np.log1p(rain)

    # Approximations simples
    data["temp_3d_avg"] = temp_max
    data["temp_7d_avg"] = temp_max
    data["humidity_3d_avg"] = humidity
    data["humidity_7d_avg"] = humidity
    data["wind_3d_avg"] = wind_max
    data["wind_7d_avg"] = wind_max
    data["rain_3d_sum"] = rain * 3
    data["rain_7d_sum"] = rain * 7
    data["et0_7d_sum"] = et0 * 7
    data["vpd_7d_avg"] = vpd_max

    # Heatwave
    data["hot_day_38"] = int(temp_max >= 38)
    data["hot_day_40"] = int(temp_max >= 40)
    data["hot_day_42"] = int(temp_max >= 42)

    data["hot_days_38_rolling"] = consecutive_hot_days_38
    data["hot_days_40_rolling"] = max(consecutive_hot_days_38 - 1, 0)

    data["cumulative_heat_stress"] = (temp_max * 7) - (humidity * 0.5)
    data["heatwave_intensity"] = max(consecutive_hot_days_38, 0) + max(temp_max - 38, 0)
    data["consecutive_hot_days_38"] = consecutive_hot_days_38

    return data


def predict_risk(
    temp_max,
    humidity,
    wind_max,
    rain,
    et0,
    vpd_max,
    radiation,
    temp_min=None,
    temp_mean=None,
    consecutive_hot_days_38=0,
):
    model, features, scaler, model_name = load_artifacts()

    input_dict = build_features(
        temp_max=temp_max,
        humidity=humidity,
        wind_max=wind_max,
        rain=rain,
        et0=et0,
        vpd_max=vpd_max,
        radiation=radiation,
        temp_min=temp_min,
        temp_mean=temp_mean,
        consecutive_hot_days_38=consecutive_hot_days_38,
    )

    X_input = pd.DataFrame([input_dict])

    for col in features:
        if col not in X_input.columns:
            X_input[col] = 0

    X_input = X_input[features]
    X_input = X_input.replace([np.inf, -np.inf], np.nan).fillna(0)

    if scaler is not None:
        X_input = scaler.transform(X_input)

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X_input)[0][1]
    else:
        pred = model.predict(X_input)[0]
        proba = float(pred)

    risk_level, risk_score = risk_probability_to_level(proba)
    confidence = abs(proba - 0.5) * 2 * 100

    return {
        "model_name": model_name,
        "probability_high_risk": round(float(proba), 4),
        "risk_score": round(float(risk_score), 1),
        "risk_level": risk_level,
        "confidence": round(float(confidence), 1),
    }


if __name__ == "__main__":
    result = predict_risk(
        temp_max=41,
        humidity=18,
        wind_max=28,
        rain=0,
        et0=7.8,
        vpd_max=3.2,
        radiation=25.5,
        consecutive_hot_days_38=6
    )
    print(result)