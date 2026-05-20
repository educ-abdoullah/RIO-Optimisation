from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd
import streamlit as st

from app import config
from app.services.api_client import ApiHealth, post_prediction


@dataclass
class PredictionResult:
    source: str
    predicted_sales: float | None
    predicted_roi: float | None
    total_budget: float
    estimated_sales_from_roi: float | None = None
    calculated_roi_from_sales: float | None = None
    error: str | None = None


@st.cache_resource(show_spinner=False)
def load_model(path):
    if not path.exists():
        return None, f"Modèle absent : {path}"
    try:
        import joblib

        return joblib.load(path), None
    except ModuleNotFoundError:
        return None, "Le package joblib n'est pas disponible dans l'environnement Streamlit."
    except Exception as exc:
        return None, f"Impossible de charger {path.name} : {exc}"


def build_payload(tv: float, radio: float, social_media: float, influencer: str) -> dict[str, Any]:
    return {
        "tv": float(tv),
        "radio": float(radio),
        "social_media": float(social_media),
        "influencer": influencer,
    }


def input_dataframe(payload: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame([payload])


def validate_payload(payload: dict[str, Any]) -> str | None:
    if payload["influencer"] not in config.INFLUENCERS:
        return "Type d'influenceur invalide."
    if payload["tv"] < 0 or payload["radio"] < 0 or payload["social_media"] < 0:
        return "Les budgets doivent être positifs ou nuls."
    if payload["tv"] + payload["radio"] + payload["social_media"] == 0:
        return "Le budget total est égal à zéro. Saisissez au moins un budget positif."
    return None


def predict_sales(payload: dict[str, Any], api_url: str, health: ApiHealth) -> PredictionResult:
    total_budget = payload["tv"] + payload["radio"] + payload["social_media"]
    validation_error = validate_payload(payload)
    if validation_error:
        return PredictionResult("validation", None, None, total_budget, error=validation_error)

    if health.available and health.sales_model_loaded:
        result, error = post_prediction(api_url, "/predict/sales", payload)
        if result:
            return PredictionResult(
                source="API",
                predicted_sales=float(result["predicted_sales"]),
                predicted_roi=None,
                total_budget=float(result["total_budget"]),
                calculated_roi_from_sales=result.get("calculated_roi_from_sales"),
            )
        api_error = error
    else:
        api_error = health.message or "API indisponible"

    model, model_error = load_model(config.SALES_MODEL_PATH)
    if model is None:
        return PredictionResult("local", None, None, total_budget, error=model_error or api_error)

    try:
        prediction = float(model.predict(input_dataframe(payload))[0])
        return PredictionResult(
            source="modèle local",
            predicted_sales=round(prediction, 2),
            predicted_roi=None,
            total_budget=round(total_budget, 2),
            calculated_roi_from_sales=round(prediction / total_budget, 4),
        )
    except Exception as exc:
        return PredictionResult("local", None, None, total_budget, error=f"Erreur de prédiction Sales : {exc}")


def predict_roi(payload: dict[str, Any], api_url: str, health: ApiHealth) -> PredictionResult:
    total_budget = payload["tv"] + payload["radio"] + payload["social_media"]
    validation_error = validate_payload(payload)
    if validation_error:
        return PredictionResult("validation", None, None, total_budget, error=validation_error)

    if health.available and health.roi_model_loaded:
        result, error = post_prediction(api_url, "/predict/roi", payload)
        if result:
            return PredictionResult(
                source="API",
                predicted_sales=None,
                predicted_roi=float(result["predicted_roi"]),
                total_budget=float(result["total_budget"]),
                estimated_sales_from_roi=result.get("estimated_sales_from_roi"),
            )
        api_error = error
    else:
        api_error = health.message or "API indisponible"

    model, model_error = load_model(config.ROI_MODEL_PATH)
    if model is None:
        return PredictionResult("local", None, None, total_budget, error=model_error or api_error)

    try:
        prediction = float(model.predict(input_dataframe(payload))[0])
        return PredictionResult(
            source="modèle local",
            predicted_sales=None,
            predicted_roi=round(prediction, 4),
            total_budget=round(total_budget, 2),
            estimated_sales_from_roi=round(prediction * total_budget, 2),
        )
    except Exception as exc:
        return PredictionResult("local", None, None, total_budget, error=f"Erreur de prédiction ROI : {exc}")
