from enum import Enum, auto
from typing import Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class LinkType(Enum):
    ALL = auto()
    INTERNAL = auto()
    EXTERNAL = auto()


class LinkExtractor:
    @staticmethod
    def scrape_url(
        url: str, link_type: LinkType = LinkType.ALL, **kwargs
    ) -> Set[str]:
        """
        Scrape a given URL for unique links within a specified element, with an option to choose between internal, external, or all links.
        Converts relative URLs to absolute URLs.
        :param url: The URL of the website to scrape.
        :param link_type: The type of links to scrape (LinkType.ALL, LinkType.INTERNAL, LinkType.EXTERNAL).
        :param kwargs: Keyword arguments to specify element id and element type.
        :return: A set of unique link URLs found within the specified element.
        """
        element_id = kwargs.get("element_id")
        element_type = kwargs.get("element_type", "nav")
        base_url = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(url))

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            if element_id:
                fetched_element = soup.find_all(element_type, id=element_id)
            else:
                fetched_element = soup.find_all(element_type)

            links = set()

            # Iterate over all found elements and extract links
            for element in fetched_element:
                for a_tag in element.find_all("a", href=True):
                    href = a_tag["href"]
                    absolute_url = urljoin(url, href)
                    domain = urlparse(absolute_url).netloc

                    if (
                        link_type == LinkType.INTERNAL
                        and domain == urlparse(base_url).netloc
                    ):
                        links.add(absolute_url)
                    elif (
                        link_type == LinkType.EXTERNAL
                        and domain != urlparse(base_url).netloc
                    ):
                        links.add(absolute_url)
                    elif link_type == LinkType.ALL:
                        links.add(absolute_url)

            return links
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            return set()
        except Exception as e:
            print(f"An error occurred: {e}")
            return set()
