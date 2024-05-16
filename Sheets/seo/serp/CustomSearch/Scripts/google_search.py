import requests
import json
import time
import csv
import logging
import os
from dotenv import load_dotenv
load_dotenv('/Users/tis/foam/cdp/code/cfg/.env')


# Configure logging
logging.basicConfig(level=logging.INFO)

# Google Custom Search API limitations
MAX_RESULTS = 100  # The API allows up to 100 results for a query

def fetch_google_search_results(api_key, cx_id, query, start=1):
    """Fetch search results using Google's Custom Search API."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx_id,
        'q': query,
        'start': start
    }
    response = requests.get(url, params=params)
    return response.json()

def main():
    # Replace with your actual API key and CX ID
    API_KEY = os.getenv('GOOGLE_API_KEY')
    CX_ID = os.getenv('CX_ID')
    
    # Hard-coded domain to search
    domain = "example.com"
    query = f"site:{domain}"
    
    start_index = 1
    
    # Specify output directory and CSV file name
    output_directory = "code/function/seo/data/out/custom_search"
    os.makedirs(output_directory, exist_ok=True)
    csv_file_name = f"{output_directory}/{domain}_search_results.csv"
    
    # Create or open a CSV file and write the header
    with open(csv_file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['URL'])
    
    for start_index in range(1, MAX_RESULTS, 10):  # API returns 10 results at a time
        logging.info(f"Fetching results starting from index {start_index}...")
        
        results = fetch_google_search_results(API_KEY, CX_ID, query, start=start_index)
        
        if 'items' not in results:
            logging.info("No more results found.")
            break
        
        # Append URLs to the CSV file
        with open(csv_file_name, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for item in results['items']:
                logging.info(f"Found URL: {item['link']}")
                csvwriter.writerow([item['link']])
        
        # Sleep for 2 seconds to handle rate limiting
        logging.info("Sleeping for 2 seconds to handle rate limiting...")
        time.sleep(2)

if __name__ == "__main__":
    main()
