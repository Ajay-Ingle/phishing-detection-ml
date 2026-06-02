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

def fit_model(    x_train: pd.DataFrame,
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

    # Log tags and parameters to the active MLflow run (managed by caller)
    mlflow.set_tag("developer", "Ajay")
    mlflow.set_tag("branch", "dev")
    mlflow.set_tag("stage", "experimentation")
    mlflow.set_tag("model_type", "XGBoost")

    # Log hyperparameters
    mlflow.log_params(hyperparameters)

    # Train the model
    model = XGBClassifier(**hyperparameters)
    model.fit(x_train, y_train)

    # Log the trained model to the active run
    mlflow.xgboost.log_model(
        xgb_model=model,
        name="xgboost_model"
    )

    print("\nModel training complete and logged to MLflow.")

    return model



