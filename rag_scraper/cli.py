import argparse

from rag_scraper.converter import Converter
from rag_scraper.link_extractor import LinkExtractor
from rag_scraper.scraper import Scraper
from rag_scraper.utils import URLUtils


def main():
    parser = argparse.ArgumentParser(
        description="RAGScraper: A tool to scrape, extract links, and convert webpages to markdown."
    )

    parser.add_argument("url", help="The URL of the webpage to scrape.")
    parser.add_argument(
        "--element_id",
        help="The ID of the element to search for links.",
        default=None,
    )
    parser.add_argument(
        "--element_type",
        help='The type of the element to search for links. Default is "nav".',
        default="nav",
    )
    parser.add_argument(
        "--convert",
        help="Convert the webpage to markdown.",
        action="store_true",
    )
    parser.add_argument(
        "--extract",
        help="Extract links from the specified element.",
        action="store_true",
    )

    args = parser.parse_args()

    base_url = URLUtils.get_base_url(args.url)

    if args.extract:
        # Extract links if the flag is set
        links = LinkExtractor.scrape_url(
            args.url,
            element_id=args.element_id,
            element_type=args.element_type,
        )
        print(f"Unique links for {args.url}:")
        for link in links:
            print(link)
    elif args.convert:
        # Convert to markdown if the flag is set
        html_content = Scraper.fetch_html(args.url)
        markdown_content = Converter.html_to_markdown(html_content, base_url)
        print(markdown_content)
    else:
        print(
            "Please specify an action: --convert for markdown conversion or --extract for link extraction."
        )


if __name__ == "__main__":
    main()
