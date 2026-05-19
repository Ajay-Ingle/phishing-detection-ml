# orchestration
# src/training/pipeline.py
import os
import joblib
import mlflow
import mlflow.xgboost

from sklearn.model_selection import train_test_split
from src.training import train, evaluate

def run_training_pipeline(data_path: str, model_output_dir: str):
    """Orchestrates structural step tasks handling framework data runs recursively."""
    print("Initializing architecture execution pipeline verification processes...")
    
    # 1. Data Ingestion Step Execution
    raw_data = train.load_data(data_path)
    # feature engineering
    X, y = train.prepare_features_and_targets(raw_data)
    
    # 2. Dataset Isolation Partition Splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # hyperparameters
    hyperparameters = {
        'n_estimators': 100,
        'max_depth': 50,
        'learning_rate': 0.1,
        'eval_metric': 'mlogloss'
    }

    # mlflow experiment setup
    mlflow.set_experiment("Phishing_Detection")

    with mlflow.start_run(run_name="xgboost_pipeline_v1"):
        # tags
        mlflow.set_tag("developer","Ajay")
        mlflow.set_tag("branch", "dev")
        mlflow.set_tag("stage", "training")
        mlflow.set_tag("model_type","XGBoost")
        mlflow.log_params(hyperparameters)

        # model training
        trained_estimator = train.fit_model(X_train, y_train, hyperparameters)

        # Predictions
        predictions = trained_estimator.predict(X_test)

        #metrics evaluation
        scores = evaluate.calculate_metrics(y_test, predictions)

        for metric_name, score_value in scores.items():
            print(f"{metric_name.title()}: {score_value:.4f}")
            mlflow.log_metric(metric_name, score_value) 
        

            # 7. Save Local Model Artifact
            os.makedirs(model_output_dir, exist_ok=True)

            target_destination_path = os.path.join(
                model_output_dir,
                "XGBoostClassifier.pickle.dat"
            )

        joblib.dump(trained_estimator, target_destination_path)

            # 8. Log Model To MLflow
        model_info = mlflow.xgboost.log_model(
                xgb_model=trained_estimator,
                name="xgboost_model"
            )
        model_uri = model_info.model_uri

        mlflow.register_model(
            model_uri=model_uri,
            name="phishing_detector"
        )

            # 9. Log Serialized Artifact
        mlflow.log_artifact(target_destination_path)

        print(
                f"\nPipeline Run Finalized. "
                f"Metrics Verified. "
                f"Weight Saved to: {target_destination_path}"
            )

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )

    DATASET_SOURCE = os.path.join(
        BASE_DIR,
        "dataset",
        "CombinedDataset.csv"
    )

    OUTPUT_DESTINATION = os.path.join(
        BASE_DIR,
        "models"
        )

    run_training_pipeline(
        DATASET_SOURCE,
        OUTPUT_DESTINATION
        )       
    
    