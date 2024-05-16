import csv
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from requests.sessions import Session

def extract_links_from_sitemap(url, session):
    try:
        response = session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            urls = soup.find_all('loc')
            return [url.text for url in urls]
        else:
            print(f"Failed to fetch sitemap from {url}")
            return []
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return []

def extract_all_links(sitemap_urls):
    all_links = []
    with Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(extract_links_from_sitemap, url, session) for url in sitemap_urls]
            for future in concurrent.futures.as_completed(futures):
                links = future.result()
                all_links.extend(links)
    return all_links

def save_to_csv(links):
    with open('urls.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL'])
        for link in links:
            writer.writerow([link])

# Define sitemap_urls with the list of URLs you provided
sitemap_urls = [
    "https://somalab.us/sitemap_products_1.xml?from=6792351023158&to=6967572693046",
    "https://somalab.us/sitemap_pages_1.xml",
    "https://somalab.us/sitemap_collections_1.xml",
    "https://somalab.us/sitemap_blogs_1.xml"
]

# Extracting all links from sitemaps
all_links = extract_all_links(sitemap_urls)

# Save links to CSV
save_to_csv(all_links)

print("URLs saved")
