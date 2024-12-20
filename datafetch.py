import requests
import pandas as pd

# API Endpoint and Key
api_key = "fe9881f343b94da096d207e46cc31c8e"  # Replace with your API key
url = "https://newsapi.org/v2/everything"

# Define Parameters
params = {
    "q": "supply chain disruption",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 100  
}

# Make API Request
response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"}, params=params)

# Check if request is successful
if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])
    
    # Extract relevant data into a DataFrame
    df = pd.DataFrame([{
        "title": article["title"],
        "description": article["description"],
        "publishedAt": article["publishedAt"],
        "source": article["source"]["name"],
        "url": article["url"]
    } for article in articles])
    
    print(df.head())  # Display the data
    df.to_csv("supply_chain_newsA.csv", index=False)
else:
    print(f"Error: {response.status_code}, {response.text}")















    NXVkDPnRv9SLGQIwH6LhngXP5j0lniic
