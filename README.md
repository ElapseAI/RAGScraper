# RAGScraper

RAGScraper is a simple Python package that scrapes webpages and converts them to markdown format for RAG usage.

## Installation

To install RAGScraper, simply run:

```bash
pip install ragscraper
```

## Usage

To use RAGScraper as a command-line tool:

```bash
rag-scraper <URL>
```

To use RAGScraper in a Python script:

```python
from rag_scraper.scraper import Scraper
from rag_scraper.converter import Converter

# Fetch HTML content
url = "https://example.com"
html_content = Scraper.fetch_html(url)

# Convert to Markdown
markdown_content = Converter.html_to_markdown(
    html=html_content, 
    base_url=base_url,
    parser_features='html.parser', 
    ignore_links=True
)
print(markdown_content)
```

## Development

To run the tests for RAGScraper, navigate to the package directory and run:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.