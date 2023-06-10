import requests

from bs4 import BeautifulSoup

target_url = 'https://example.com'

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

            

            if url and url.startswith('https://example.com') and url not in visited_urls:

                crawl_frontier.append(url)

    

    visited_urls.add(current_url)

    

    if len(current_url.split('/')) - 2 >= max_depth:

        continue

