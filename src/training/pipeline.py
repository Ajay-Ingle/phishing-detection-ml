# orchestration
# src/training/pipeline.py
import os
import joblib
from sklearn.model_selection import train_test_split
from src.training import train, evaluate

def run_training_pipeline(data_path: str, model_output_dir: str):
    """Orchestrates structural step tasks handling framework data runs recursively."""
    print("Initializing architecture execution pipeline verification processes...")
    
    # 1. Data Ingestion Step Execution
    raw_data = train.load_data(data_path)
    X, y = train.prepare_features_and_targets(raw_data)
    
    # 2. Dataset Isolation Partition Splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Fit Target Estimator Structure 
    trained_estimator = train.fit_model(X_train, y_train, X_test, y_test)
    
    # 4. Metric Diagnostics Verification Validation Check
    predictions = trained_estimator.predict(X_test)
    scores = evaluate.calculate_metrics(y_test, predictions)
    
    print("\n--- Pipeline Deployment Performance Metrics Report ---")
    for metric_name, score_value in scores.items():
        print(f"{metric_name.title()}: {score_value:.4f}")
        
    # 5. Model Serialization Artifact Export Generation Action
    os.makedirs(model_output_dir, exist_ok=True)
    target_destination_path = os.path.join(model_output_dir, "XGBoostClassifier.pickle.dat")
    joblib.dump(trained_estimator, target_destination_path)
    print(f"\nPipeline Run Finalized. Metrics Verified. Weight Saved to: {target_destination_path}")

if __name__ == "__main__":
    # Baseline setup pointing to standard repository structure positions
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATASET_SOURCE = os.path.join(BASE_DIR, "dataset", "CombinedDataset.csv")
    OUTPUT_DESTINATION = os.path.join(BASE_DIR, "models")
    
    run_training_pipeline(DATASET_SOURCE, OUTPUT_DESTINATION)