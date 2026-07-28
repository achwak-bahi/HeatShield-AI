"""
HeatShield AI - Feature Engineering
Création de variables intelligentes pour la prédiction du risque d'incendie.
"""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "algeria_weather_clean_v1.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "algeria_weather_features_v1.csv"


def load_data(path=INPUT_FILE):
    """Charge le dataset nettoyé."""
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["wilaya_nom", "date"]).reset_index(drop=True)
    return df


def add_basic_interactions(df):
    """Ajoute des interactions simples entre variables météo."""
    df["heat_humidity_ratio"] = df["temp_max"] / (df["humidity"] + 1)
    df["wind_drought_index"] = df["wind_max"] * (df["et0"] + 1)
    df["dry_air_index"] = df["vpd_max"] * (1 + (df["temp_max"] / 100))
    df["rain_protection"] = np.log1p(df["rain"])
    return df


def add_rolling_features(df):
    """Ajoute des moyennes glissantes par wilaya."""
    group = df.groupby("wilaya_nom")

    df["temp_3d_avg"] = group["temp_max"].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df["temp_7d_avg"] = group["temp_max"].transform(lambda x: x.rolling(7, min_periods=1).mean())
    df["humidity_3d_avg"] = group["humidity"].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df["humidity_7d_avg"] = group["humidity"].transform(lambda x: x.rolling(7, min_periods=1).mean())
    df["wind_3d_avg"] = group["wind_max"].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df["wind_7d_avg"] = group["wind_max"].transform(lambda x: x.rolling(7, min_periods=1).mean())
    df["rain_3d_sum"] = group["rain"].transform(lambda x: x.rolling(3, min_periods=1).sum())
    df["rain_7d_sum"] = group["rain"].transform(lambda x: x.rolling(7, min_periods=1).sum())
    df["et0_7d_sum"] = group["et0"].transform(lambda x: x.rolling(7, min_periods=1).sum())
    df["vpd_7d_avg"] = group["vpd_max"].transform(lambda x: x.rolling(7, min_periods=1).mean())

    return df


def add_heatwave_features(df):
    """Ajoute des indicateurs de canicule."""
    df["hot_day_38"] = (df["temp_max"] >= 38).astype(int)
    df["hot_day_40"] = (df["temp_max"] >= 40).astype(int)
    df["hot_day_42"] = (df["temp_max"] >= 42).astype(int)

    group = df.groupby("wilaya_nom")

    df["hot_days_38_rolling"] = group["hot_day_38"].transform(lambda x: x.rolling(7, min_periods=1).sum())
    df["hot_days_40_rolling"] = group["hot_day_40"].transform(lambda x: x.rolling(7, min_periods=1).sum())

    df["cumulative_heat_stress"] = (
        df["temp_max"].rolling(7, min_periods=1).sum()
        - (df["humidity"].rolling(7, min_periods=1).mean() * 0.5)
    )

    df["heatwave_intensity"] = (
        (df["temp_max"] - df["temp_7d_avg"]).clip(lower=0)
        + (df["hot_days_38_rolling"] * 0.8)
    )

    return df


def add_consecutive_hot_days(df):
    """Compte les jours consécutifs de forte chaleur par wilaya."""
    consecutive = []
    for _, g in df.groupby("wilaya_nom", sort=False):
        count = 0
        vals = []
        for hot in g["hot_day_38"]:
            if hot == 1:
                count += 1
            else:
                count = 0
            vals.append(count)
        consecutive.extend(vals)

    df["consecutive_hot_days_38"] = consecutive
    return df


def add_risk_labels(df):
    """Conserve risk_score et risk_level + ajoute version binaire."""
    df["high_risk_binary"] = (df["risk_score"] >= 50).astype(int)
    return df


def finalize_features(df):
    """Nettoie et sélectionne les colonnes utiles pour le ML."""
    cols_to_fill = [
        "temp_3d_avg", "temp_7d_avg",
        "humidity_3d_avg", "humidity_7d_avg",
        "wind_3d_avg", "wind_7d_avg",
        "rain_3d_sum", "rain_7d_sum",
        "et0_7d_sum", "vpd_7d_avg",
        "hot_days_38_rolling", "hot_days_40_rolling",
        "cumulative_heat_stress", "heatwave_intensity",
        "consecutive_hot_days_38"
    ]

    for col in cols_to_fill:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    return df


def main():
    print("=" * 60)
    print("🔥 HeatShield AI — Feature Engineering")
    print("=" * 60)

    df = load_data()
    print(f"📂 Chargé: {len(df)} lignes")

    df = add_basic_interactions(df)
    df = add_rolling_features(df)
    df = add_heatwave_features(df)
    df = add_consecutive_hot_days(df)
    df = add_risk_labels(df)
    df = finalize_features(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Sauvegardé: {OUTPUT_FILE}")
    print(f"Shape final: {df.shape}")
    print("Nouvelles colonnes:")
    new_cols = [
        c for c in df.columns
        if c not in [
            'date','temp_max','temp_min','temp_mean','humidity','wind_max','rain',
            'et0','vpd_max','radiation','wilaya_code','wilaya_nom','latitude',
            'longitude','year','risk_score','risk_level'
        ]
    ]
    print(new_cols)
    print("=" * 60)


if __name__ == "__main__":
    main()