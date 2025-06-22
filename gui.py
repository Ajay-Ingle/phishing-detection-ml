import tkinter as tk
from tkinter import messagebox
import joblib
from feature_extractor import feature_extraction
import whois

# Load trained model
model = joblib.load('XGBoostClassifier.pickle.dat')

def check_url():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Input Error", "Please enter a URL.")
        return

    try:
        # WHOIS info (you can handle exceptions for unregistered domains)
        try:
            domain_info = whois.whois(url)
        except:
            domain_info = {}

        # Extract features
        features = feature_extraction(url, domain_info)
        
        # Prediction
        prediction = model.predict([features])[0]
        prediction_text = "🔒 Legitimate Website" if prediction == 0 else "⚠️ Phishing Website"

        # Display output
        result_label.config(text=prediction_text, fg="green" if prediction == 0 else "red")

        # Display features
        feature_output = "\n".join([f"Feature {i+1}: {val}" for i, val in enumerate(features)])
        features_text.delete("1.0", tk.END)
        features_text.insert(tk.END, feature_output)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Phishing URL Detector")
root.geometry("600x500")
root.configure(bg="#f5f5f5")

# URL input label and entry
tk.Label(root, text="Enter URL:", font=("Arial", 14), bg="#f5f5f5").pack(pady=(20, 5))
url_entry = tk.Entry(root, width=60, font=("Arial", 12))
url_entry.pack(pady=5)

# Check Button
check_button = tk.Button(root, text="Check URL", font=("Arial", 12), bg="#4CAF50", fg="white", command=check_url)
check_button.pack(pady=10)

# Prediction Result
result_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#f5f5f5")
result_label.pack(pady=10)

# Feature Values Label
tk.Label(root, text="Feature Values (0/1):", font=("Arial", 13, "underline"), bg="#f5f5f5").pack()

# Feature Values Output Box
features_text = tk.Text(root, height=15, width=60, font=("Courier", 10))
features_text.pack(pady=5)

root.mainloop()
