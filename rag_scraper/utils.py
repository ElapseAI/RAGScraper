from urllib.parse import urljoin, urlparse


class URLUtils:
    @staticmethod
    def get_base_url(url: str) -> str:
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"

    @staticmethod
    def resolve_url(src: str, base_url: str) -> str:
        return urljoin(base_url, src)
