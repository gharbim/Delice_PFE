"""summary.py — Volume forecasting backtest summary.

Loads the historical Automobile monthly volume (2014-2018 growth phase) and the 2018 backtest
forecast comparison produced in PYTHON_SCRIPT/ML/notebooks/07_volume_forecasting.ipynb, once at
import time, and exposes a summary for the dashboard.

Note: this is a BACKTEST on the portfolio's growth phase, not a live forecast for the present —
the model was deliberately trained and evaluated only on 2014-2017/2018 data (see notebook 07 for
why the fuller history, which includes a later decline, was excluded).
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

_history_df = pd.read_csv(ARTIFACTS_DIR / "monthly_emission_volume_growth_phase.csv")
_forecast_df = pd.read_csv(ARTIFACTS_DIR / "monthly_volume_forecast.csv")
_sarima_model = joblib.load(ARTIFACTS_DIR / "volume_forecast_model.joblib")

_MODEL_COLUMNS = {
    "SeasonalNaive": "forecast_SeasonalNaive",
    "HoltWinters": "forecast_HoltWinters",
    "SARIMA": "forecast_SARIMA",
}

FUTURE_HORIZON = 6

# Fold the known 2018 actuals into the fitted model's state (no re-estimation) so that
# get_forecast() below produces genuinely unseen months beyond the dataset's last known
# point (2018-12), rather than replaying the already-known 2018 backtest.
_actuals_index = pd.DatetimeIndex(pd.to_datetime(_forecast_df["month"]), freq="MS", name="month")
_actuals_series = pd.Series(_forecast_df["actual"].values, index=_actuals_index, name="nb_quittances")
_sarima_extended = _sarima_model.append(_actuals_series, refit=False)


def _mape(actual, pred) -> float:
    actual, pred = np.array(actual), np.array(pred)
    return float(np.mean(np.abs((actual - pred) / actual)) * 100)


def _compute_metrics() -> list:
    actual = _forecast_df["actual"].values
    metrics = []
    for name, col in _MODEL_COLUMNS.items():
        pred = _forecast_df[col].values
        mae = float(np.mean(np.abs(actual - pred)))
        rmse = float(np.sqrt(np.mean((actual - pred) ** 2)))
        metrics.append({
            "model": name,
            "mae": round(mae, 1),
            "rmse": round(rmse, 1),
            "mape": round(_mape(actual, pred), 1),
        })
    return metrics


def _compute_future(n: int = FUTURE_HORIZON) -> list:
    fc = _sarima_extended.get_forecast(n)
    mean, ci = fc.predicted_mean, fc.conf_int()
    return [
        {
            "month": month.strftime("%Y-%m-%d"),
            "forecast": round(float(mean.iloc[i]), 1),
            "ci_lower": round(float(ci.iloc[i, 0]), 1),
            "ci_upper": round(float(ci.iloc[i, 1]), 1),
        }
        for i, month in enumerate(mean.index)
    ]


def get_forecast_summary() -> dict:
    history = [
        {"month": row["month"], "actual": int(row["nb_quittances"])}
        for _, row in _history_df.iterrows()
    ]

    ci = _sarima_model.get_forecast(12).conf_int()
    ci_lower = ci.iloc[:, 0].values
    ci_upper = ci.iloc[:, 1].values

    test = []
    for i, (_, row) in enumerate(_forecast_df.iterrows()):
        test.append({
            "month": row["month"],
            "actual": int(row["actual"]),
            "forecast_seasonal_naive": round(float(row["forecast_SeasonalNaive"]), 1),
            "forecast_holt_winters": round(float(row["forecast_HoltWinters"]), 1),
            "forecast_sarima": round(float(row["forecast_SARIMA"]), 1),
            "ci_lower": round(float(ci_lower[i]), 1),
            "ci_upper": round(float(ci_upper[i]), 1),
        })

    metrics = _compute_metrics()
    future = _compute_future()

    last_actual = history[-1]
    next_future = future[0]
    pct_change = (next_future["forecast"] - last_actual["actual"]) / last_actual["actual"] * 100
    trend = "up" if pct_change > 3 else "down" if pct_change < -3 else "steady"

    headline = {
        "last_actual_month": last_actual["month"],
        "last_actual_value": last_actual["actual"],
        "next_month": next_future["month"],
        "next_month_forecast": round(next_future["forecast"]),
        "next_month_low": round(next_future["ci_lower"]),
        "next_month_high": round(next_future["ci_upper"]),
        "pct_change": round(pct_change, 1),
        "trend": trend,
    }

    sarima_mape = next(m["mape"] for m in metrics if m["model"] == "SARIMA")
    accuracy_note = (
        f"Lors des tests sur les données réelles de 2018, cette méthode de prévision se situait "
        f"généralement à environ {round(sarima_mape)}% du volume mensuel réel."
    )

    return {
        "success": True,
        "scope_note": (
            "Ceci est une prévision de démonstration construite sur l'historique 2014-2018 du "
            "portefeuille Automobile. Les mois après décembre 2018 sont la propre projection du "
            "modèle au-delà du dernier point de données connu."
        ),
        "accuracy_note": accuracy_note,
        "headline": headline,
        "history": history,
        "future": future,
        "test": test,
        "metrics": metrics,
    }
