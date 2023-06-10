import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

if len(sys.argv) < 2:
    print("Please provide the target URLs as command-line arguments.")
    print("Usage: python crawl.py <target_url1> <target_url2> ...")
    sys.exit(1)

target_urls = sys.argv[1:]
crawl_frontier = target_urls[:]
visited_urls = set()
max_depth = 3

while crawl_frontier:
    current_url = crawl_frontier.pop(0)

    if current_url in visited_urls:
        continue

    # Prepend "https://" if no scheme is provided
    parsed_url = urlparse(current_url)
    if not parsed_url.scheme:
        current_url = "https://" + current_url

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

            if url:
                # Handle relative URLs and convert them to absolute URLs
                absolute_url = urljoin(response.url, url)

                if absolute_url not in visited_urls:
                    crawl_frontier.append(absolute_url)

    visited_urls.add(current_url)

    if len(current_url.split('/')) - 2 >= max_depth:
        continue
