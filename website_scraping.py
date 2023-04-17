import requests
from bs4 import BeautifulSoup
import re

def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        # Remove excessive whitespace
        text = re.sub('\s+', ' ', text)
        # Split text into paragraphs and add line breaks
        text = '\n\n'.join([p.strip() for p in text.split('\n') if p.strip()])
        return text
    except requests.exceptions.RequestException as e:
        print("Failed to scrape website.")
        print(str(e))
        return ""
