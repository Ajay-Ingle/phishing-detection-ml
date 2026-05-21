# src/inference/model_loader.py
import os
from typing import Any

import mlflow
import mlflow.pyfunc

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

class ModelLoaderSingleton:
    """Thread-safe loader managing an MLflow-registry-backed model instance."""
    _instance = None
    _model = None

def load_production_model():
    model_uri = f"models:/{MODEL_NAME}/3"
    model = mlflow.pyfunc.load_model(model_uri)
    print(f"Model loaded from MLflow registry: {model_uri}")
    return model

def load_model(self, model_uri: str) -> Any:
    """Load a model from the MLflow registry into memory once."""
    if self._model is None:
        if not model_uri:
            raise ValueError("A valid MLflow model URI is required.")
        self._model = mlflow.pyfunc.load_model(model_uri)
        print(f"Model loaded from MLflow registry: {model_uri}")
    return self._model
