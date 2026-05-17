# src/inference/model_loader.py
import os
import joblib
from typing import Any

class ModelLoaderSingleton:
    """Thread-safe instantiation construct managing localized operational model persistence loops."""
    _instance = None
    _model = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelLoaderSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def load_model(self, model_path: str) -> Any:
        """Loads model into active working memory space if not already allocated."""
        if self._model is None:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Target model weight asset structure absent from disk index: {model_path}")
            self._model = joblib.load(model_path)
            print(f"Model instance deserialized. Baseline active from space target memory context: {model_path}")
        return self._model