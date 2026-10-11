"""predict.py — Auto insurance premium pricing model.

Loads the trained pipeline (preprocessing + XGBoost regressor) built in
PYTHON_SCRIPT/ML/notebooks/04_premium_pricing_model.ipynb once at import time,
and exposes a single prediction function for the pricing API endpoint.

Note: the pipeline was trained on `premium_sim`, a documented, formula-based
simulated premium (see notebook 02) — the real DWH premium has no relationship
with these risk factors. This model demonstrates the pricing methodology, not
a real market price.
"""
import json
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

pipeline = joblib.load(ARTIFACTS_DIR / "premium_pricing_pipeline.joblib")

with open(ARTIFACTS_DIR / "premium_pricing_metadata.json") as f:
    metadata = json.load(f)

NUMERIC_FEATURES = metadata["numeric_features"]
CATEGORICAL_FEATURES = metadata["categorical_features"]
FEATURE_ORDER = NUMERIC_FEATURES + CATEGORICAL_FEATURES

LIB_USAGE_CHOICES = [
    "Affaires",
    "Agric. - de 3T50",
    "Agric. + de 3T50",
    "Util. - de 3T50",
    "Util. + de 3T50",
    "TPM - de 3T50",
    "TPV",
    "Eng. Agr. Cat1",
]

# The 22 Tunisian governorates present in dwh.dim_client.ville.
ALL_CITIES = [
    "Tunis", "Sfax", "Sousse", "Kairouan", "Bizerte", "Gabes", "Ariana",
    "Gafsa", "Monastir", "Medenine", "Nabeul", "Tataouine", "Beja",
    "Jendouba", "Mahdia", "Siliana", "Le Kef", "Sidi Bouzid",
    "Zaghouan", "Tozeur", "Kebili", "Manouba",
]

# Same urban/rest grouping used to build `city_risk_tier` in notebook 02 —
# kept here as the single source of truth so the API and the training
# pipeline never drift apart.
URBAN_CITIES = {"Tunis", "Sfax", "Sousse", "Ariana", "Nabeul", "Monastir"}


def predict_price(payload: dict) -> float:
    row = dict(payload)
    row["city_risk_tier"] = 1 if row.pop("ville") in URBAN_CITIES else 0
    df = pd.DataFrame([{feature: row[feature] for feature in FEATURE_ORDER}])
    prediction = pipeline.predict(df)
    return float(prediction[0])
