# predict.py

import pickle
import whois
from urllib.parse import urlparse

from feature_extractor import feature_extraction

# Load the trained model (make sure the path is correct)
with open("XGBoostClassifier.pickle.dat", "rb") as f:
    model = pickle.load(f)

# Get URL from user
url = input("Enter the URL to check: ")

# Parse WHOIS info
try:
    domain_info = whois.whois(urlparse(url).netloc)
except:
    domain_info = None

# Extract features
features = feature_extraction(url, domain_info)

# Predict (reshaping for single sample)
result = model.predict([features])[0]

# Output
if result == 1:
    print("⚠️  The URL is **Phishing**.")
else:
    print("✅ The URL is **Legitimate**.")
