import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Please provide the target URL as a command-line argument.")
    print("Usage: python crawl.py <target_url>")
    sys.exit(1)

target_url = sys.argv[1]
crawl_frontier = [target_url]
visited_urls = set()
max_depth = 3

while crawl_frontier:
    current_url = crawl_frontier.pop(0)
    
    try:
        response = requests.get(current_url)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {current_url}: {e}")
        continue

    if response.status_code != 200:
        print(f"Request to {current_url} returned status code {response.status_code}")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')
    print(f"Title: {soup.title.string}")
    
    if response.headers.get('Content-Type', '').startswith('text/html'):
        links = soup.find_all('a')
        
        for link in links:
            url = link.get('href')
