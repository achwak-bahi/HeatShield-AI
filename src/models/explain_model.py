"""
HeatShield AI - Explainability
Extraction de l'importance des variables du meilleur modèle.
"""

from pathlib import Path

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "models"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

MODEL_FILE = MODEL_DIR / "best_model.pkl"
FEATURES_FILE = MODEL_DIR / "feature_names.pkl"
BEST_MODEL_NAME_FILE = MODEL_DIR / "best_model_name.txt"

OUTPUT_IMPORTANCE = DATA_PROCESSED / "feature_importance.csv"


def load_artifacts():
    model = joblib.load(MODEL_FILE)
    features = joblib.load(FEATURES_FILE)

    best_model_name = "unknown"
    if BEST_MODEL_NAME_FILE.exists():
        best_model_name = BEST_MODEL_NAME_FILE.read_text(encoding="utf-8").strip()

    return model, features, best_model_name


def extract_feature_importance(model, features):
    """Extrait l'importance si disponible."""
    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_
        df_imp = pd.DataFrame({
            "feature": features,
            "importance": importance
        }).sort_values(by="importance", ascending=False)
        return df_imp

    return pd.DataFrame(columns=["feature", "importance"])


def main():
    print("=" * 60)
    print("🔥 HeatShield AI — Explainability")
    print("=" * 60)

    model, features, best_model_name = load_artifacts()
    print(f"Meilleur modèle: {best_model_name}")
    print(f"Nombre de features: {len(features)}")

    df_imp = extract_feature_importance(model, features)

    if df_imp.empty:
        print("⚠️ Le modèle ne fournit pas directement feature_importances_.")
        return

    df_imp.to_csv(OUTPUT_IMPORTANCE, index=False)

    print("\nTop 15 features importantes:")
    print(df_imp.head(15))

    print(f"\n✅ Sauvegardé: {OUTPUT_IMPORTANCE}")
    print("=" * 60)


if __name__ == "__main__":
    main()