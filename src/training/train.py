# To train the model:
# dataset loading
# train-test split
# model training
# model fitting

# src/training/train.py
import mlflow
import mlflow.xgboost
from mlflow.tracking import MlflowClient

import pandas as pd
from typing import Tuple, Dict, Any

from sklearn.model_selection import train_test_split
from sklearn.metrics import(
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from xgboost import XGBClassifier

# DATA LOADING
def load_data(file_path: str) -> pd.DataFrame:
    """
    Reads data from local storage into dataframe.
    """
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

# model training and experiment tracking
def fit_model(
        x_train: pd.DataFrame,
        y_train: pd.Series,
        x_test: pd.DataFrame,
        y_test: pd.Series,
        hyperparameters: Dict[str, Any] = None
)-> XGBClassifier:
    
    if hyperparameters is None:
        hyperparameters = {
            "learning_rate": 0.2,
            "max_depth": 5,
            "n_estimators": 50,
            "eval_metric": "mlogloss"
        }

    #MLFlow experiment

    mlflow.set_experiment("Phishing_detection")

    with mlflow.start_run(
        run_name="xgboost_baseline_v2"
    ) as run:
        mlflow.set_tag("developer","Ajay")
        mlflow.set_tag("branch","dev")
        mlflow.set_tag("stage", "experimentation")
        mlflow.set_tag("model_type", "XGBoost")

        #log parameters
        mlflow.log_params(hyperparameters)

        #Train the model
        model = XGBClassifier(**hyperparameters)
        model.fit(x_train, y_train)

        #Predictions
        predictions = model.predict(x_test)

        #metrics
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions)
        recall = recall_score(y_test, predictions)
        f1 = f1_score(y_test, predictions)

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)

        #log the model
        mlflow.xgboost.log_model(
            xgb_model = model,
            name = "xgboost_model"
        )

        model_uri = f"runs:/{run.info.run_id}/xgboost_model"
        registered_model = mlflow.register_model(
            model_uri = model_uri,
            name = "phishing_detector",
        )

        client = MlflowClient()
        client.transition_model_version_stage(
            name = registered_model.name,
            version = registered_model.version,
            stage = "Production",
            archive_existing_versions = True
        )

        # print results
        print("\n Experiment metrics--")
        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision : {precision:.4f}")
        print(f"Recall : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")

    return model