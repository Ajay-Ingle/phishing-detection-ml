from prometheus_client import Counter

prediction_counter = Counter(
    "phishing_predictions_total",
    "Total phishing prediction requests"
)

phishing_counter = Counter(
    "phishing_urls_detected_total",
    "Total phishing URLs detected"
)
