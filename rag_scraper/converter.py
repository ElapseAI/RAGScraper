import re
from typing import Optional
from urllib.parse import urljoin

import html2text
from bs4 import BeautifulSoup, Tag


class Converter:
    @staticmethod
    def html_to_markdown(
        html: str,
        base_url: str,
        parser_features="html.parser",
        **conversion_options,
    ) -> str:
        soup = BeautifulSoup(html, parser_features)
        cleaned_soup = Converter.replace_media_with_markdown(soup, base_url)
        return Converter.convert_html_to_markdown(
            str(cleaned_soup), **conversion_options
        )

    @staticmethod
    def replace_media_with_markdown(
        soup: BeautifulSoup, base_url: str
    ) -> BeautifulSoup:
        data_uri_pattern = re.compile(
            r"data:([a-zA-Z]+/[a-zA-Z+.-]+)?(;base64)?,[^,]*"
        )

        def process_media_tag(tag: Tag, media_type: str) -> Optional[str]:
            media_url = tag.get("src", "")
            if data_uri_pattern.match(media_url):
                tag.decompose()
                return None
            if not media_url.startswith(("http://", "https://")):
                media_url = urljoin(base_url, media_url.lstrip("/"))
            alt_text = f"{media_type}: {tag.get('alt', '') or tag.get('title', '')}".strip()
            return f"![{alt_text}]({media_url})"

        for img in soup.find_all("img"):
            markdown_img = process_media_tag(img, "Image")
            if markdown_img:
                img.replace_with(markdown_img)

        for video in soup.find_all("video"):
            markdown_video = process_media_tag(video, "Video")
            if markdown_video:
                video.replace_with(markdown_video)

        return soup

    @staticmethod
    def convert_html_to_markdown(cleaned_html: str, **options) -> str:
        converter = html2text.HTML2Text()
        for key, value in options.items():
            setattr(converter, key, value)
        return converter.handle(cleaned_html)
