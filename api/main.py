from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import os

#api
app = FastAPI(
    title="Marketing ROI Prediction API",
    description="API de prédiction des ventes à partir des budgets marketing",
    version="1.0.0"
)

#load model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_sales_model.joblib")

try:
    model = joblib.load(MODEL_PATH)
    model_loaded = True
except Exception as e:
    model = None
    model_loaded = False
    load_error = str(e)

class MarketingInput(BaseModel):
    tv: float = Field(..., ge=0, description="Budget TV en million")
    radio: float = Field(..., ge=0, description="Budget Radio en million")
    social_media: float = Field(..., ge=0, description="Budget Social Media en million")
    influencer: str = Field(..., description="Type d'influenceur : Mega, Macro, Micro ou Nano")

@app.get("/health")
def health_check():
    if model_loaded:
        return {
            "status": "ok",
            "model_loaded": True
        }
    else:
        return {
            "status": "error",
            "model_loaded": False,
            "error": load_error
        }


@app.get("/model-info")
def model_info():
    return {
        "model_name": "Best regression model",
        "target": "sales",
        "features": ["tv", "radio", "social_media", "influencer"],
        "task": "Regression",
        "output": "Predicted sales"
    }


@app.post("/predict")
def predict(data: MarketingInput):
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Le modèle n'est pas chargé correctement."
        )

    try:
        # Vérification du type d'influenceur
        allowed_influencers = ["Mega", "Macro", "Micro", "Nano"]

        if data.influencer not in allowed_influencers:
            raise HTTPException(
                status_code=400,
                detail=f"influencer doit être l'une des valeurs suivantes : {allowed_influencers}"
            )

        # Transformation de l'entrée en DataFrame
        input_df = pd.DataFrame([{
            "tv": data.tv,
            "radio": data.radio,
            "social_media": data.social_media,
            "influencer": data.influencer
        }])

        # Prédiction
        prediction = model.predict(input_df)[0]

        # Calcul du budget total et du ROI estimé
        total_budget = data.tv + data.radio + data.social_media

        if total_budget > 0:
            estimated_roi = prediction / total_budget
        else:
            estimated_roi = None

        return {
            "input": {
                "tv": data.tv,
                "radio": data.radio,
                "social_media": data.social_media,
                "influencer": data.influencer
            },
            "predicted_sales": round(float(prediction), 2),
            "total_budget": round(float(total_budget), 2),
            "estimated_roi": round(float(estimated_roi), 4) if estimated_roi is not None else None
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la prédiction : {str(e)}"
        )