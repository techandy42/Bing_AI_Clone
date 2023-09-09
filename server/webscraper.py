import requests
from bs4 import BeautifulSoup

def fetch_webpage_content(url):
    # Send HTTP request
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title_tag = soup.find('title')
        title_text = title_tag.string if title_tag else "No title found"

        # Remove script, style, header, and footer elements
        for unwanted_tag in soup(['script', 'style', 'header', 'footer']):
            unwanted_tag.extract()

        # Extract text from the remaining HTML
        text = soup.get_text()

        # Remove leading and trailing whitespace and condense all whitespace to a single space
        clean_text = " ".join(text.split())

        return clean_text, title_text
    else:
        return f"Failed to fetch content. HTTP Status Code: {response.status_code}", None