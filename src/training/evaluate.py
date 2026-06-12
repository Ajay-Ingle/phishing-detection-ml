# metrices

# src/training/evaluate.py
import numpy as np
import pandas as pd
from typing import Dict, Any
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def calculate_metrics(y_true: pd.Series, y_pred: np.ndarray) -> Dict[str, float]:
    """Performs mathematical diagnostic scoring verification cascades over predictions."""
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average='binary', zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average='binary', zero_division=0)),
        "f1_score": float(f1_score(y_true, y_pred, average='binary', zero_division=0))
    }