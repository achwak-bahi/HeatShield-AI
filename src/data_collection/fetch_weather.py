"""
HeatShield AI - Collecte des données météo via Open-Meteo API
API gratuite, sans clé API.
"""

import sys
import time
from pathlib import Path

import pandas as pd
import requests

# Pour importer wilayas.py depuis le même dossier
sys.path.insert(0, str(Path(__file__).parent))
from wilayas import get_all_wilayas

# ═══════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════
YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
START_MD = "05-01"  # début période estivale
END_MD = "10-31"    # fin période estivale

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = OUTPUT_DIR / "algeria_weather_raw.csv"

API_URL = "https://archive-api.open-meteo.com/v1/archive"

DAILY_VARS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "wind_speed_10m_max",
    "precipitation_sum",
    "et0_fao_evapotranspiration",
    "vapour_pressure_deficit_max",
    "shortwave_radiation_sum",
]


def fetch_one_wilaya_one_year(wilaya, year):
    """Récupère les données quotidiennes pour UNE wilaya et UNE année."""
    start_date = f"{year}-{START_MD}"
    end_date = f"{year}-{END_MD}"

    params = {
        "latitude": wilaya["lat"],
        "longitude": wilaya["lon"],
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(DAILY_VARS),
        "timezone": "Africa/Algiers",
    }

    try:
        r = requests.get(API_URL, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()

        if "daily" not in data:
            print(f"  ⚠️ Pas de 'daily' pour {wilaya['nom']} {year}")
            return None

        df = pd.DataFrame(data["daily"])
        df["wilaya_code"] = wilaya["code"]
        df["wilaya_nom"] = wilaya["nom"]
        df["latitude"] = wilaya["lat"]
        df["longitude"] = wilaya["lon"]
        df["year"] = year
        return df

    except Exception as e:
        print(f"  ❌ Erreur {wilaya['nom']} {year}: {e}")
        return None


def fetch_all(wilayas=None, years=None):
    """Boucle sur toutes les wilayas et années. Sauvegarde finale."""
    if wilayas is None:
        wilayas = get_all_wilayas()
    if years is None:
        years = YEARS

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    frames = []
    total = len(wilayas) * len(years)
    done = 0

    print("=" * 60)
    print("🔥 HeatShield AI — Collecte Open-Meteo")
    print(f"   Wilayas: {len(wilayas)} | Années: {years}")
    print(f"   Requêtes: {total}")
    print(f"   Sortie: {OUTPUT_FILE}")
    print("=" * 60)

    for w in wilayas:
        print(f"\n📍 {w['code']} — {w['nom']}")
        for y in years:
            done += 1
            print(f"   [{done}/{total}] {y}...", end=" ")
            df = fetch_one_wilaya_one_year(w, y)
            if df is not None and len(df) > 0:
                frames.append(df)
                print(f"OK ({len(df)} jours)")
            else:
                print("VIDE/ERREUR")
            time.sleep(0.6)

        # Sauvegarde partielle après chaque wilaya
        if frames:
            tmp = pd.concat(frames, ignore_index=True)
            tmp.to_csv(OUTPUT_DIR / "algeria_weather_raw_partial.csv", index=False)

    if not frames:
        print("\n❌ Aucune donnée récupérée.")
        return None

    final = pd.concat(frames, ignore_index=True)
    final.to_csv(OUTPUT_FILE, index=False)

    print("\n" + "=" * 60)
    print("✅ TERMINÉ")
    print(f"   Lignes: {len(final)}")
    print(f"   Fichier: {OUTPUT_FILE}")
    print("=" * 60)
    return final


# ═══════════════════════════════════════════
# MODE TEST — 1 wilaya, 1 année (rapide)
# ═══════════════════════════════════════════
if __name__ == "__main__":
    # FULL RUN: toutes les wilayas, toutes les années
    fetch_all()