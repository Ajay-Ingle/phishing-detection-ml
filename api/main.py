from fastapi import FastAPI
from api.schemas.request_shema import URLRequest
from src.inference.predict import predict_url


app = FastAPI(
    title = "Phishing Detection MLOps API"
)

@app.get("/health")
def health_check():
    return{"status": "API is healthy"}

@app.post("/predict")
def predict(request: URLRequest):
    result = predict_url(request.url)
    return result