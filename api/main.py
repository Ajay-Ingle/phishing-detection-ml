from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os

from src.inference.predict import predict_url

app = FastAPI()        # ← THIS LINE WAS MISSING


@app.get("/")
def home():
    return {"message": "API running"}


class PredictRequest(BaseModel):
    url: str
    model_uri: Optional[str] = None


@app.post("/predict")
def predict(req: PredictRequest):
    """Accepts a JSON body with `url` and optional `model_uri`, returns prediction."""
    model_uri = req.model_uri or os.getenv("MLFLOW_MODEL_URI", "models:/phishing_detector/Production")
    try:
        outcome = predict_url(req.url, model_uri)
    except Exception as exc:
        return {"success": False, "error": str(exc)}

    return {
        "success": True,
        "url": req.url,
        "prediction": int(outcome),
        "assessment": "⚠️ PHISHING DETECTED" if int(outcome) == 1 else "🔒 SAFE/LEGITIMATE",
    }