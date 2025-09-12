import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env variables")

genai.configure(api_key=api_key)
print("API key loaded successfully") # check if API key loaded successfully

model = genai.GenerativeModel("gemini-2.5-flash")

json_file = "/Users/enricatan/Documents/techcrawler/recent_tech_articles.json"

try:
    with open(json_file, 'r') as f: # f is a temporary variable for the file object 
        data =json.load(f) # turns the json file into a dictionary
        print("File loaded successfully")

except FileNotFoundError:
    print(f"File {json_file} not found")

except json.JSONDecodeError:
    print(f"Error: Invalid JSON in {json_file}")


prompt = f"""
You are a helpful assistant that summarizes tech news articles.

Here are the news articles:
{json.dumps(data, indent=4)}

Please summarize the news articles in a concise and informative way."""

try:
    response = model.generate_content(prompt)
    print(response.text)
except Exception as e:
    print(f"Error generating summary: {e}")