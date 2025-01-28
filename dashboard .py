import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import smtplib
from email.mime.text import MIMEText

# Load the combined supply chain risk data
data = pd.read_csv("final_combined_data.csv")

# Flask app for the dashboard
app = Flask(__name__)

# Slack integration
SLACK_TOKEN = "xoxb-Your-Slack-Token-Here"
SLACK_CHANNEL = "#supply-chain-alerts"
slack_client = WebClient(token=SLACK_TOKEN)

# Email integration
EMAIL_ADDRESS = "venishakumar509@gmail.com"
EMAIL_PASSWORD = "your-email-password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Function to send Slack notifications
def send_slack_notification(message):
    try:
        slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        print("Slack notification sent successfully!")
    except SlackApiError as e:
        print(f"Error sending Slack notification: {e.response['error']}")

# Function to send email notifications
def send_email_notification(subject, body, recipient_email):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Error sending email notification: {e}")

# Flask route for the dashboard
@app.route("/")
def dashboard():
    # Generate visualizations
    plt.figure(figsize=(10, 6))
    sns.countplot(data=data, x="Risk_Level", palette="viridis")
    plt.title("Risk Level Distribution")
    plt.xlabel("Risk Level")
    plt.ylabel("Count")
    plt.savefig("static/risk_distribution.png")
    plt.close()

    inventory_data = data.groupby("Supplier ID")["Inventory_Status"].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=inventory_data, x="Supplier ID", y="Inventory_Status", palette="coolwarm")
    plt.title("Inventory Status by Supplier")
    plt.xlabel("Supplier ID")
    plt.ylabel("Inventory Status")
    plt.xticks(rotation=45)
    plt.savefig("static/inventory_status.png")
    plt.close()

    # Filter critical disruptions
    critical_disruptions = data[data["Risk_Level"] == "High"]
    if not critical_disruptions.empty:
        # Send alerts
        slack_message = f"⚠️ Critical Risk Alert: {len(critical_disruptions)} disruptions detected!"
        send_slack_notification(slack_message)
        send_email_notification(
            "Critical Risk Alert",
            f"Detected {len(critical_disruptions)} critical disruptions in the supply chain.",
            "team@example.com"
        )

    return render_template("dashboard.html", disruptions=critical_disruptions)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
