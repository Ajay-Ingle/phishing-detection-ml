import threading
import mlflow

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
                    print(f"Fetching model from URI: {model_uri}...")
                    # Dynamically downloads and loads the tracked production artifact
                    self._model = mlflow.pyfunc.load_model(model_uri)
                    print("Model successfully loaded into memory.")
        return self._model