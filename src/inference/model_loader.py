import os
import threading
import mlflow
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ModelLoaderSingleton:
    """Thread-safe loader managing an MLflow-registry-backed model instance."""
    _instance = None
    _model = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def load_model(self, model_uri: str):
        """
        Loads the model from the MLflow registry if it hasn't been loaded yet,
        or returns the cached model instance from memory.
        """
        if self._model is None:
            with self._lock:
                if self._model is None:
                    # Configure MLflow tracking URI from environment
                    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
                    if tracking_uri:
                        mlflow.set_tracking_uri(tracking_uri)
                        print(f"✓ MLflow tracking URI configured: {tracking_uri}")
                    else:
                        print("⚠ MLFLOW_TRACKING_URI not set. Using default MLflow configuration.")
                    
                    print(f"Fetching model from URI: {model_uri}...")
                    # Dynamically downloads and loads the tracked production artifact
                    self._model = mlflow.pyfunc.load_model(model_uri)
                    print("Model successfully loaded into memory.")
        return self._model