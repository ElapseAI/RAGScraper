from typing import Set

import requests
from bs4 import BeautifulSoup


class LinkExtractor:
    @staticmethod
    def scrape_url(url: str, **kwargs) -> Set[str]:
        """
        Scrape a given URL for all unique links within a specified element.

        :param url: The URL of the website to scrape.
        :param kwargs: Keyword arguments to specify element id and element type.
        :return: A set of unique link URLs found within the specified element.
        """
        element_id = kwargs.get("element_id")
        element_type = kwargs.get("element_type", "nav")

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            fetched_element = soup.find(element_type, id=element_id)
            links = fetched_element.find_all("a") if fetched_element else []
            return set(link.get("href") for link in links)
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            return set()
        except Exception as e:
            print(f"An error occurred: {e}")
            return set()
