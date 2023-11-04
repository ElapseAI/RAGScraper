import requests
from bs4 import BeautifulSoup


class Scraper:
    @staticmethod
    def fetch_html(url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def get_soup(html_content: str, **parser_options) -> BeautifulSoup:
        return BeautifulSoup(html_content, "html.parser", **parser_options)
