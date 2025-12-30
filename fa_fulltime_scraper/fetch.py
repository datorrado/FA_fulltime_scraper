from curl_cffi import requests
from bs4 import BeautifulSoup



def fetch_html(url:str) -> BeautifulSoup:

    """
    Fetches html from the FA link using a browser-like client, returning a beatifulSoup object (tree to extract all info from the page)
    """

    session = requests.Session()

    response = session.get(url, impersonate="chrome120")

    response.raise_for_status()

    html = response.text
    if len(html) < 10_000:
        raise ValueError("HTML is a little short, possible error loading")
    
    return BeautifulSoup(html, "html.parser")

