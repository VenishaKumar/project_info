from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd;

try:
    Token = "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"
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", token=Token, legacy=False)
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf", token=Token)
    print("Model and tokenizer loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

# Function to analyze sentiment using LLaMA
def analyze_sentiment(text):
    if not isinstance(text, str) or not text.strip():
        return "Neutral", 0  # Default for missing or empty text

    prompt = f"Analyze the sentiment of the following text and categorize it as Positive, Negative, or Neutral: {text}"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(inputs["input_ids"], max_length=512, num_beams=5)
    sentiment = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    if "Positive" in sentiment:
        return "Positive", 0  # Low Risk
    elif "Negative" in sentiment:
        return "Negative", 1  # High Risk
    else:
        return "Neutral", 0  # Low Risk

# Load datasets
supplier_data = pd.read_csv("large_supplier_data.csv")
transport_data = pd.read_csv("large_transportation_datas.csv")
news_data = pd.read_csv("microchip_news_data.csv")

# Add columns for risk analysis
news_data["Sentiment"], news_data["Risk_Score"] = zip(*news_data["Description"].apply(analyze_sentiment))
news_data["Risk_Level"] = news_data["Risk_Score"].apply(lambda x: "High" if x == 1 else "Low")

# Ensure consistent Supplier ID data type
supplier_data["Supplier ID"] = supplier_data["Supplier ID"].astype(str)
transport_data["Supplier ID"] = transport_data["Supplier ID"].astype(str)
news_data["Supplier ID"] = news_data["Supplier ID"].astype(str)

# Merge data
merged_supplier_news = pd.merge(supplier_data, news_data, on="Supplier ID", how="left")
final_data = pd.merge(merged_supplier_news, transport_data, on="Supplier ID", how="left")
print(final_data)

# Save final data
final_data.to_csv("final_combined_data.csv", index=False)
print("Final combined data with risk analysis saved to 'final_combined_data.csv'.")
