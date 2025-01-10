import requests
import pandas as pd

# Replace with your News API key
API_KEY = 'fe9881f343b94da096d207e46cc31c8e'
BASE_URL = "https://newsapi.org/v2/everything"

# Function to fetch news articles about microchips
def fetch_microchip_news(query, page_size=100):
    params = {
        'q': query,  # Search for "microchip"
        'apiKey': API_KEY,
        'pageSize': page_size,  # Number of results per page
        'language': 'en'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if data["status"] == "ok":
        return data["articles"]
    else:
        return []

# Fetch news about microchips
microchip_news = fetch_microchip_news("microchip", page_size=3000)

# Extract relevant fields from the news data
microchip_data = []
for i, article in enumerate(microchip_news, start=1):
    microchip_data.append({
        "Supplier ID": f"S{i:04d}",  # Generate Supplier ID like S0001, S0002, etc.
        "Title": article['title'],
        "Description": article['description'],
        "Source": article['source']['name'],
        "Content": article['content'],
        "Published At": article['publishedAt'],
        "URL": article['url']
    })

# Convert the data to a DataFrame
microchip_df = pd.DataFrame(microchip_data)

# Save the data to a CSV file
microchip_file_path = "microchip_news_datas.csv"
microchip_df.to_csv(microchip_file_path, index=False)

print(f"Microchip news data saved to: {microchip_file_path}")
