from datetime import datetime
import pandas as pd

# Load data with predictions
data = pd.read_csv("data_with_disruption_predictions.csv")

# Function to generate stock adjustment recommendations
def generate_stock_adjustments(row):
    if row["Predicted_Disruption_Risk"] == 1:  # High Risk
        return {
            "Supplier ID": row["Supplier ID"],
            "Action": "Increase Buffer Stock",
            "Recommended Qty": int(row["Current_Stock"] * 1.2)  # Increase by 20%
        }
    else:
        return {
            "Supplier ID": row["Supplier ID"],
            "Action": "Maintain Current Levels",
            "Recommended Qty": row["Current_Stock"]
        }

# Generate recommendations
data["Current_Stock"] = data["Current_Stock"].fillna(100)  # Default stock level
adjustments = data.apply(generate_stock_adjustments, axis=1)
adjustments_df = pd.DataFrame(list(adjustments))

# Save adjustments to a file
adjustments_df.to_csv("stock_adjustments.csv", index=False)
print("Stock adjustments saved to 'stock_adjustments.csv'.")

# ERP Integration Example
def integrate_with_erp(adjustments):
    for _, adjustment in adjustments.iterrows():
        # Simulate ERP update
        print(f"ERP Update - Supplier ID: {adjustment['Supplier ID']}, "
              f"Action: {adjustment['Action']}, "
              f"Recommended Qty: {adjustment['Recommended Qty']}")
    print("ERP integration completed.")

integrate_with_erp(adjustments_df)
