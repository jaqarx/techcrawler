import os
import json
from dotenv import load_dotenv # Loads environment variables from .env file
import google.generativeai as genai
from flask import Flask, render_template, jsonify # Flask is a web framework for Python

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env variables")

genai.configure(api_key=api_key) # This is how you give the Gemini API key to the client
print("API key loaded successfully") # Check if API key loaded successfully
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__) # Create a Flask instance, __name__ is the standard to initialize Flask

# Load tech articles from the JSON file
def get_tech_articles():
    json_file = "/Users/florayasmin/techcrawler/recent_tech_articles.json"
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"File {json_file} not found")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {json_file}")
        return []

# Generate a summary of the tech articles
def generate_summary(articles):
    prompt = f"""
    You are a helpful assistant that summarizes tech news articles.
    
    Here are the news articles:
    {json.dumps(articles, indent=4)}

    Please summarize the news articles in a concise and informative way."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

# Define a route for the home page to display the summary
@app.route('/')
def index():
    """Main page with the summary"""
    articles = get_tech_articles()
    summary = generate_summary(articles)

    return render_template('index.html',
                           summary=summary,
                           articles=articles,
                           article_count=len(articles))

# Define an API route to return summary data in JSON format
@app.route('/api/summary')
def api_summary():
    """API endpoint to return the summary as JSON"""
    articles = get_tech_articles()
    summary = generate_summary(articles)

    return jsonify({
        'summary': summary,
        'article_count': len(articles),
        'articles': articles
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) # Server is publicly available, accessible from any IP address
    # Specify port number (ex. 127.0.0.1:8080) if entering IP address into web browser