from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="Marketing ROI Prediction API",
    description="API pour prédire les ventes et le ROI à partir des budgets marketing",
    version="2.0.0",
)

BASE_DIR = Path(__file__).resolve().parent.parent

SALES_MODEL_PATH = BASE_DIR / "models" / "best_sales_model.joblib"
ROI_MODEL_PATH = BASE_DIR / "models" / "best_roi_model.joblib"
ALLOWED_INFLUENCERS = ["Mega", "Macro", "Micro", "Nano"]


try:
    sales_model = joblib.load(SALES_MODEL_PATH)
    sales_model_loaded = True
    sales_model_error = None
except Exception as exc:
    sales_model = None
    sales_model_loaded = False
    sales_model_error = str(exc)

try:
    roi_model = joblib.load(ROI_MODEL_PATH)
    roi_model_loaded = True
    roi_model_error = None
except Exception as exc:
    roi_model = None
    roi_model_loaded = False
    roi_model_error = str(exc)


class MarketingInput(BaseModel):
    tv: float = Field(..., ge=0, description="Budget TV")
    radio: float = Field(..., ge=0, description="Budget Radio")
    social_media: float = Field(..., ge=0, description="Budget Social Media")
    influencer: str = Field(..., description="Type d'influenceur : Mega, Macro, Micro ou Nano")


def payload_dump(data: MarketingInput) -> dict:
    if hasattr(data, "model_dump"):
        return data.model_dump()
    return data.dict()


def input_to_dataframe(data: MarketingInput) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "tv": data.tv,
                "radio": data.radio,
                "social_media": data.social_media,
                "influencer": data.influencer,
            }
        ]
    )


def validate_influencer(influencer: str) -> None:
    if influencer not in ALLOWED_INFLUENCERS:
        raise HTTPException(
            status_code=400,
            detail=f"influencer doit être parmi : {ALLOWED_INFLUENCERS}",
        )


@app.get("/health")
def health():
    return {
        "status": "ok" if sales_model_loaded and roi_model_loaded else "partial_error",
        "sales_model_loaded": sales_model_loaded,
        "roi_model_loaded": roi_model_loaded,
        "sales_model_error": sales_model_error,
        "roi_model_error": roi_model_error,
    }


@app.get("/model-info")
def model_info():
    return {
        "features": ["tv", "radio", "social_media", "influencer"],
        "routes": {
            "/predict/sales": "Prédiction des ventes",
            "/predict/roi": "Estimation du ROI",
        },
        "models": {
            "sales_model": {
                "target": "sales",
                "format": "joblib",
                "path": str(SALES_MODEL_PATH),
            },
            "roi_model": {
                "target": "roi",
                "format": "joblib",
                "path": str(ROI_MODEL_PATH),
            },
        },
    }


@app.post("/predict/sales")
def predict_sales(data: MarketingInput):
    validate_influencer(data.influencer)

    if sales_model is None:
        raise HTTPException(
            status_code=500,
            detail=f"Le modèle Sales n'est pas chargé : {sales_model_error}",
        )

    try:
        input_df = input_to_dataframe(data)
        predicted_sales = float(sales_model.predict(input_df)[0])

        total_budget = data.tv + data.radio + data.social_media
        calculated_roi = predicted_sales / total_budget if total_budget > 0 else None

        return {
            "prediction_type": "sales",
            "predicted_sales": round(predicted_sales, 2),
            "total_budget": round(total_budget, 2),
            "calculated_roi_from_sales": round(calculated_roi, 4) if calculated_roi is not None else None,
            "input": payload_dump(data),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la prédiction Sales : {exc}",
        )


@app.post("/predict/roi")
def predict_roi(data: MarketingInput):
    validate_influencer(data.influencer)

    if roi_model is None:
        raise HTTPException(
            status_code=500,
            detail=f"Le modèle ROI n'est pas chargé : {roi_model_error}",
        )

    try:
        input_df = input_to_dataframe(data)
        predicted_roi = float(roi_model.predict(input_df)[0])

        total_budget = data.tv + data.radio + data.social_media
        estimated_sales_from_roi = predicted_roi * total_budget

        return {
            "prediction_type": "roi",
            "predicted_roi": round(predicted_roi, 4),
            "total_budget": round(total_budget, 2),
            "estimated_sales_from_roi": round(estimated_sales_from_roi, 2),
            "input": payload_dump(data),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la prédiction ROI : {exc}",
        )
