# src/training/train.py
import pandas as pd

from typing import Tuple, Dict, Any

from xgboost import XGBClassifier

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
        hyperparameters= {
            'n_estimators': 100,
            'max_depth': 5,
            'learning_rate': 0.1,
            'eval_metric': 'logloss'
        }
    model = XGBClassifier(**hyperparameters)
    model.fit(x_train, y_train)
    return model



