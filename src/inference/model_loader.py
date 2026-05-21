# src/inference/model_loader.py
import os
from typing import Any

import mlflow
import mlflow.pyfunc

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://host.docker.internal:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

class ModelLoaderSingleton:
    """Thread-safe loader managing an MLflow-registry-backed model instance."""
    _instance = None
    _model = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelLoaderSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def load_model(self, model_uri: str) -> Any:
        """Load a model from the MLflow registry into memory once."""
        if self._model is None:
            if not model_uri:
                raise ValueError("A valid MLflow model URI is required.")
            self._model = mlflow.pyfunc.load_model(model_uri)
            print(f"Model loaded from MLflow registry: {model_uri}")
        return self._model