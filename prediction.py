import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load and prepare data
data = pd.read_csv("final_combined_data.csv")

# Feature Engineering
# Convert categorical data to numeric
data["Category_Encoded"] = data["Category"].astype("category").cat.codes
data["Risk_Level_Encoded"] = data["Risk_Level"].map({"Low": 0, "High": 1})

# Select features and target
features = ["Category_Encoded", "Risk_Score", "Transport_Delay", "Supplier_Reliability"]
target = "Risk_Level_Encoded"

X = data[features].fillna(0)  # Replace missing values with 0
y = data[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train predictive model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Model Evaluation Report:")
print(classification_report(y_test, y_pred))

# Save model for future use
import joblib
joblib.dump(model, "disruption_predictor_model.pkl")
print("Disruption predictor model saved as 'disruption_predictor_model.pkl'.")

# Predict disruptions
data["Predicted_Disruption_Risk"] = model.predict(X)
data.to_csv("data_with_disruption_predictions.csv", index=False)
print("Data with disruption predictions saved to 'data_with_disruption_predictions.csv'.")
