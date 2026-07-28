"""
HeatShield AI - Calcul du score et du niveau de risque d'incendie
Prototype basé sur les variables météo collectées via Open-Meteo.
"""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "algeria_weather_raw.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "algeria_weather_with_risk.csv"


def rename_columns(df):
    """Renomme les colonnes Open-Meteo en noms courts."""
    mapping = {
        "time": "date",
        "temperature_2m_max": "temp_max",
        "temperature_2m_min": "temp_min",
        "temperature_2m_mean": "temp_mean",
        "relative_humidity_2m_mean": "humidity",
        "wind_speed_10m_max": "wind_max",
        "precipitation_sum": "rain",
        "et0_fao_evapotranspiration": "et0",
        "vapour_pressure_deficit_max": "vpd_max",
        "shortwave_radiation_sum": "radiation",
    }
    return df.rename(columns=mapping)


def compute_risk_score(row):
    """Calcule un score de risque entre 0 et 100."""
    temp = row.get("temp_max", np.nan)
    hum = row.get("humidity", np.nan)
    wind = row.get("wind_max", np.nan)
    rain = row.get("rain", np.nan)
    et0 = row.get("et0", np.nan)
    vpd = row.get("vpd_max", np.nan)

    if pd.isna(temp) or pd.isna(hum):
        return np.nan

    score = 0.0

    # Température
    if temp >= 45:
        score += 40
    elif temp >= 42:
        score += 35
    elif temp >= 38:
        score += 28
    elif temp >= 34:
        score += 18
    elif temp >= 30:
        score += 10
    elif temp >= 26:
        score += 4

    # Humidité
    if hum <= 15:
        score += 30
    elif hum <= 25:
        score += 24
    elif hum <= 35:
        score += 16
    elif hum <= 45:
        score += 8
    elif hum <= 55:
        score += 3

    # Vent
    if not pd.isna(wind):
        if wind >= 40:
            score += 20
        elif wind >= 30:
            score += 15
        elif wind >= 20:
            score += 10
        elif wind >= 12:
            score += 5

    # Pluie = réduit le risque
    if not pd.isna(rain):
        if rain >= 15:
            score -= 30
        elif rain >= 8:
            score -= 20
        elif rain >= 3:
            score -= 10
        elif rain >= 1:
            score -= 4

    # Sécheresse
    if not pd.isna(et0):
        if et0 >= 9:
            score += 10
        elif et0 >= 6:
            score += 6
        elif et0 >= 4:
            score += 3

    # Déficit de pression de vapeur
    if not pd.isna(vpd):
        if vpd >= 4:
            score += 8
        elif vpd >= 2.5:
            score += 5
        elif vpd >= 1.5:
            score += 2

    score = max(0.0, min(100.0, score))
    return round(score, 1)


def score_to_level(score):
    """Convertit un score en niveau de risque."""
    if pd.isna(score):
        return "Inconnu"
    if score < 25:
        return "Faible"
    elif score < 50:
        return "Modéré"
    elif score < 75:
        return "Élevé"
    return "Critique"


def main():
    print("=" * 60)
    print("🔥 HeatShield AI — Calcul du risque")
    print("=" * 60)

    if not RAW_FILE.exists():
        print(f"❌ Fichier introuvable: {RAW_FILE}")
        return

    df = pd.read_csv(RAW_FILE)
    print(f"📂 Chargé: {len(df)} lignes")

    df = rename_columns(df)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    print("⏳ Calcul des scores...")
    df["risk_score"] = df.apply(compute_risk_score, axis=1)
    df["risk_level"] = df["risk_score"].apply(score_to_level)

    print("\n📊 Distribution des niveaux de risque:")
    print(df["risk_level"].value_counts(dropna=False))

    print(f"\nScore moyen: {df['risk_score'].mean():.2f}")
    print(f"Score min:   {df['risk_score'].min():.2f}")
    print(f"Score max:   {df['risk_score'].max():.2f}")

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ Sauvegardé: {OUTPUT_FILE}")
    print(f"Colonnes finales: {list(df.columns)}")
    print("=" * 60)


if __name__ == "__main__":
    main()