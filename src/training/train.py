# src/training/train.py
import os
import mlflow
import mlflow.xgboost
from dotenv import load_dotenv

import pandas as pd
from typing import Tuple, Dict, Any
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from xgboost import XGBClassifier

# Load environment variables from .env file
load_dotenv()

# DATA LOADING

def load_data(file_path: str) -> pd.DataFrame:

# Reads data from local storage into dataframe.

    return pd.read_csv(file_path)

# FEATURE & TARGET SEPARATION

def prepare_features_and_targets(
df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.Series]:

 
    drop_columns = [
        col for col in ['Domain', 'Label']
        if col in df.columns
    ]

    X = df.drop(columns=drop_columns)
    y = df['Label']

    return X, y

# MODEL TRAINING

def fit_model(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    hyperparameters: Dict[str, Any] = None
) -> XGBClassifier:
    if hyperparameters is None:
        hyperparameters = {
            "learning_rate": 0.2,
            "max_depth": 5,
            "n_estimators": 50,
            "eval_metric": "mlogloss"
        }

    # Train the model
    model = XGBClassifier(**hyperparameters)
    model.fit(x_train, y_train)

    print("\nModel training complete.")
    return model


def log_and_register_model(
    model: XGBClassifier,
    name: str = "phishing_detector"
):
    """Log the trained model to MLflow and register it in the model registry."""
    model_info = mlflow.xgboost.log_model(
        xgb_model=model,
        name="xgboost_model"
    )

    mlflow.register_model(
        model_uri=model_info.model_uri,
        name=name
    )

    print(f"✓ Model logged and registered as '{name}' in MLflow Registry.")
    return model_info



