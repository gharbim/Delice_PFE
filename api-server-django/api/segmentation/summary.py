"""summary.py — Portfolio segmentation summary.

Loads the cluster assignments produced in PYTHON_SCRIPT/ML/notebooks/05_customer_segmentation.ipynb
once at import time, and exposes an aggregated, labeled summary for the dashboard.

Note: this is the real-data segmentation (notebook 05), not the simulated risk-tier comparison
(notebook 06) — these clusters reflect genuine historical claims/payment behavior, not a
constructed formula.
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

_df = pd.read_csv(ARTIFACTS_DIR / "auto_policies_segments.csv")
_total_policies = len(_df)

_cluster_stats = _df.groupby("cluster").agg(
    size=("id_police", "count"),
    avg_driver_age=("driver_age", "mean"),
    avg_vehicle_age=("vehicle_age", "mean"),
    avg_puissance=("puissance", "mean"),
    avg_bonus_malus=("bonus_malus", "mean"),
    claim_rate=("has_claim_raw", "mean"),
    avg_claim_amount=("total_claim_amount_raw", "mean"),
    impaye_rate=("has_impaye_raw", "mean"),
)

# Label clusters by their dominant real-world trait rather than hardcoding cluster
# numbers, so this stays correct if notebook 05 is re-run and the numbering shifts.
_payment_risk_cluster = _cluster_stats["impaye_rate"].idxmax()
_remaining = _cluster_stats.drop(index=_payment_risk_cluster)
_claims_active_cluster = _remaining["claim_rate"].idxmax()
_clean_cluster = _remaining.drop(index=_claims_active_cluster).index[0]

_LABELS = {
    _clean_cluster: "Contrats sains",
    _claims_active_cluster: "Sinistres fréquents",
    _payment_risk_cluster: "Risque de paiement",
}


def get_segment_summary() -> dict:
    segments = []
    for cluster_id, row in _cluster_stats.iterrows():
        segments.append({
            "cluster": int(cluster_id),
            "label": _LABELS[cluster_id],
            "size": int(row["size"]),
            "pct": round(100 * row["size"] / _total_policies, 1),
            "avg_driver_age": round(row["avg_driver_age"], 2),
            "avg_vehicle_age": round(row["avg_vehicle_age"], 2),
            "avg_puissance": round(row["avg_puissance"], 2),
            "avg_bonus_malus": round(row["avg_bonus_malus"], 2),
            "claim_rate": round(row["claim_rate"], 3),
            "avg_claim_amount": round(row["avg_claim_amount"], 2),
            "impaye_rate": round(row["impaye_rate"], 3),
        })
    segments.sort(key=lambda s: s["cluster"])
    return {"success": True, "total_policies": _total_policies, "segments": segments}
