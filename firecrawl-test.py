import os
import json # For writing to a JSON file
from dotenv import load_dotenv # Loads environment variables from .env file
from firecrawl import Firecrawl

load_dotenv()
api_key = os.getenv("FIRECRAWL_API_KEY")

print("Loaded environment variables")

if not api_key:
    raise ValueError("FIRECRAWL_API_KEY is not set in the .env variables")

firecrawl = Firecrawl(api_key=api_key) # This is how you give the Firecrawl API key to the client

search_query = "Latest tech advancements in the past week."
search_options = {
    "tbs": "qdr:w", # "time-based search" option set to "query within the last week"
    "limit": 5
}

try:
    # Calling the search function and inputting its parameters, of which were set above
    search_results = firecrawl.search(
        query=search_query,
        limit=search_options["limit"],
        tbs=search_options["tbs"]
    )
    
    print(f"Searching for: {search_query}")

    if hasattr(search_results, 'web') and search_results.web: # Scanning the search_result object for the "true" string
        print("Search successful!")
        web_results = []
        for result in search_results.web: #for-loop to iterate through every item in search_results.web and adding it to a dictionary
            web_results.append(
                {
                    'url': result.url,
                    'title': result.title,
                    'description': result.description,
                    'category': result.category
                }
            )

            with open("recent_tech_articles.json", "w") as f:
                json.dump(web_results, f, indent=2) # Creating a JSON file and dumping the list of dictionaries into it


        print("Results saved to recent_tech_articles.json")

    else:
        print("No search results found")

except Exception as e:
    print(f"An error occurred: {e}")


