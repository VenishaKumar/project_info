import requests
import pandas as pd

# Your API key
api_key = 'YOUR_API_KEY'

# API endpoint
url = 'https://api.freightos.com/v1/shippingCalculator'

# Parameters for the request
params = {
    'loadtype': 'boxes',
    'weight': 200,
    'width': 50,
    'length': 50,
    'height': 50,
    'origin': 'Shanghai, CN',
    'destination': 'New York, NY',
    'quantity': 2
}

# Headers (if needed)
headers = {
    'Authorization': f'Bearer {api_key}'
}

# Make the GET request
response = requests.get(url, params=params, headers=headers)

# Check response
if response.status_code == 200:
    try:
        data = response.json()
        df = pd.DataFrame([data])  # Convert JSON to DataFrame
        df.to_csv("freight_data.csv", index=False)
        print("Data saved to freight_data.csv")
    except ValueError:
        print("Error: Response is not JSON.")
        print(response.text)  # Debugging help
else:
    print(f"Error: {response.status_code}, Message: {response.text}")
