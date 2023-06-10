import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from tabulate import tabulate

if len(sys.argv) < 2:
    print("Please provide the target URLs as command-line arguments.")
    print("Usage: python crawl.py <target_url1> <target_url2> ...")
    sys.exit(1)

target_urls = sys.argv[1:]
crawl_frontier = target_urls[:]
visited_urls = set()
max_depth = 3

results = []

def process_url(url, base_url, visited_urls, crawl_frontier):
    if url:
        parsed_url = urlparse(url)
        if parsed_url.netloc:  # External link
            absolute_url = url
            # Add additional logic for handling external links if needed
        else:  # Internal link or relative URL
            absolute_url = urljoin(base_url, url)

        if absolute_url not in visited_urls:
            crawl_frontier.append(absolute_url)

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
        results.append([current_url, "", "", "", str(e)])
        continue

    if response.status_code != 200:
        results.append([current_url, "", "", "", f"Status Code: {response.status_code}"])
        continue

    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else ""
    results.append([current_url, title, response.headers.get('Content-Type', ''), response.url, ""])

    if response.headers.get('Content-Type', '').startswith('text/html'):
        links = soup.find_all('a')
        images = soup.find_all('img')
        scripts = soup.find_all('script')

        for link in links:
            url = link.get('href')
            process_url(url, response.url, visited_urls, crawl_frontier)

        for image in images:
            url = image.get('src')
            process_url(url, response.url, visited_urls, crawl_frontier)

        for script in scripts:
            url = script.get('src')
            process_url(url, response.url, visited_urls, crawl_frontier)

    visited_urls.add(current_url)

    if len(current_url.split('/')) - 2 >= max_depth:
        continue

table_headers = ["URL", "Title", "Content Type", "Final URL", "Error"]
print(tabulate(results, headers=table_headers, tablefmt="grid"))
