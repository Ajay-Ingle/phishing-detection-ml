# predict.py
# This file should ONLY:

# load model
# preprocess input
# return prediction

# NOT:

# UI
# Flask
# notebook code

# src/inference/predict.py
import os
import whois
from urllib.parse import urlparse

from src.features import feature_extractor
from src.inference.model_loader import ModelLoaderSingleton

DEFAULT_MLFLOW_MODEL_URI = os.getenv(
    "MLFLOW_MODEL_URI", "models:/phishing_detector/Production"
)

def predict_url(url: str, model_uri: str = DEFAULT_MLFLOW_MODEL_URI) -> int:
    """Transforms raw user configuration paths, generating target classification arrays."""
    engine = ModelLoaderSingleton()
    model = engine.load_model(model_uri)

    try:
        domain = urlparse(url).netloc
        whois_response = whois.whois(domain) if domain else None
    except Exception:
        whois_response = None

    processed_features = feature_extractor.feature_extraction(url, whois_response)
    prediction = model.predict([processed_features])[0]
    return int(prediction)

if __name__ == "__main__":
    sample_target_url = input("Enter a URL to evaluate: ")
    model_uri = os.getenv("MLFLOW_MODEL_URI", "models:/phishing_detector/Production")
    outcome = predict_url(sample_target_url, model_uri)

    print(f"\nURL Evaluated: {sample_target_url}")
    print(f"Outcome Code: {outcome}")
    print(
        f"Result Assessment: {'⚠️ PHISHING DETECTED' if outcome == 1 else '🔒 SAFE/LEGITIMATE'}"
    )
