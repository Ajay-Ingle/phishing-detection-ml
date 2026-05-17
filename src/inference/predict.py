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

def predict_url(url: str, model_directory_path: str) -> int:
    """Transforms raw user configuration paths, generating target classification arrays."""
    # 1. Access model file structure safely using the singleton pattern
    weight_path = os.path.join(model_directory_path, "XGBoostClassifier.pickle.dat")
    engine = ModelLoaderSingleton()
    model = engine.load_model(weight_path)
    
    # 2. Gather remote contextual properties
    try:
        domain = urlparse(url).netloc
        whois_response = whois.whois(domain) if domain else None
    except:
        whois_response = None
        
    # 3. Dynamic pipeline formatting
    processed_features = feature_extractor.feature_extraction(url, whois_response)
    
    # 4. Generate classifications using matching schema designs
    prediction = model.predict([processed_features])[0]
    return int(prediction)

if __name__ == "__main__":
    # Local CLI Verification Script Loop Execution
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    REPO_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
    MODELS_DIR = os.path.join(REPO_ROOT, "models")
    
    sample_target_url = input("Enter a URL to evaluate: ")
    outcome = predict_url(sample_target_url, MODELS_DIR)
    
    print(f"\nURL Evaluated: {sample_target_url}")
    print(f"Outcome Code: {outcome}")
    print(f"Result Assessment: {'⚠️ PHISHING DETECTED' if outcome == 1 else '🔒 SAFE/LEGITIMATE'}")