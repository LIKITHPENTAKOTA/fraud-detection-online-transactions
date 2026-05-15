from flask import Flask, render_template, request
import numpy as np
import joblib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Load the trained fraud detection model
model = joblib.load("rf_fraud_detection_model.pkl")

EMAIL_ADDRESS = "xxxxxxxxxxxx@gmail.com"  # 🔹 Replace with your email
EMAIL_PASSWORD = "xxxxxxxxxxxxxxxxxx"   # 🔹 Generate App Password from Google

def send_alert_email(transaction_data):
    """ Sends an email alert for fraudulent transactions. """
    recipient_email = "sushmithagulivindala@gmail.com"  # 🔹 Replace with recipient's email

    subject = "🚨 Fraudulent Transaction Alert!"
    body = f"⚠️ A fraudulent transaction was detected!\n\nTransaction Data:\n{transaction_data}"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
        server.quit()
        print("✅ Alert email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        features = []
        for i in range(1, 30):  # ✅ Expecting 29 features
            feature_value = request.form.get(f"feature{i}")  

            # 🔹 Handle missing/invalid values
            if not feature_value or feature_value.lower() == "undefined":
                return render_template("index.html", error=f"❌ Error: Missing or invalid value for Feature {i}!")

            try:
                features.append(float(feature_value))
            except ValueError:
                return render_template("index.html", error=f"❌ Error: Invalid number format for Feature {i}!")

        features_array = np.array(features).reshape(1, -1)

        if features_array.shape[1] != 29:
            return render_template("index.html", error="❌ Error: Please enter all 29 features!")

        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0][1]

        if prediction == 1:  # 🚨 Fraud detected!
            send_alert_email(features)
            result_text = "🚨 Fraudulent Transaction Detected!"
            alert_class = "alert-danger"
        else:
            result_text = "✅ Transaction is Safe"
            alert_class = "alert-success"

        return render_template(
            "index.html", prediction=result_text, probability=round(probability, 4), alert_class=alert_class
        )

    except Exception as e:
        return render_template("index.html", error=f"❌ Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)
