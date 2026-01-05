# Scrapy-Projects

A collection of web scraping tools built with Scrapy and BeautifulSoup for extracting company information from various websites.

---

## Overview

This project contains multiple web scrapers designed to:

- Extract company-related content from corporate websites
- Handle JavaScript-rendered pages using Splash
- Export data as PDF, HTML, or CSV formats
- Crawl and follow internal/external links intelligently

---

## Project Structure

```
Scrapy-Projects/
└── reportscraper/
    ├── reportscraper/
    │   ├── spiders/
    │   │   ├── __init__.py
    │   │   └── fetch_pdf_spider.py    # PDF export spider
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   ├── settings-splash.py          # Splash configuration
    │   └── 1.py                         # HTML export spider with Splash
    ├── scrapping/
    │   └── scrape_b_corp.py            # B Corp directory scraper
    └── .gitignore
```

---

## Spiders

### 1. PDF Export Spider (`fetch_pdf_spider.py`)

Extracts content from websites and exports filtered results as PDF files.

| Feature | Description |
|---------|-------------|
| Target | gallo.com |
| Output | `company_content.pdf` |
| Filter | Keyword-based content filtering |

```bash
scrapy crawl fetch_pdf
```

### 2. HTML Export Spider with Splash (`1.py`)

Crawls JavaScript-heavy websites using Splash for rendering, with intelligent link following.

| Feature | Description |
|---------|-------------|
| Target | cbrands.com |
| Output | Sequential HTML files (`2023-1.html`, `2023-2.html`, ...) |
| JS Rendering | Splash with 2s wait time |
| Link Following | Internal + relevant external links |

```bash
scrapy crawl fetch_full_content_cbrands_html_splash
```

**Excluded content:** Navigation elements, footers, privacy notices, social media links, career pages

### 3. B Corp Directory Scraper (`scrape_b_corp.py`)

Standalone BeautifulSoup script that scrapes the B Corporation directory.

| Feature | Description |
|---------|-------------|
| Target | bcorporation.net |
| Output | `b_corp_companies.csv` |
| Data | Company names and descriptions |

```bash
python scrapping/scrape_b_corp.py
```

---

## Tech Stack

- **Scrapy** — Web crawling framework
- **Scrapy-Splash** — JavaScript rendering integration
- **BeautifulSoup4** — HTML parsing
- **pdfkit** — PDF generation
- **pandas** — Data manipulation and CSV export
- **requests** — HTTP library

---

## Prerequisites

- Python 3.8+
- Docker (for Splash)
- wkhtmltopdf (for PDF generation)

---

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd Scrapy-Projects/reportscraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install scrapy scrapy-splash beautifulsoup4 pdfkit pandas requests

# Start Splash container (required for JS rendering)
docker run -p 8050:8050 scrapinghub/splash
```

---

## Configuration

### Splash Settings (`settings-splash.py`)

Ensure your `settings.py` includes Splash middleware configuration:

```python
SPLASH_URL = 'http://localhost:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
```

---

## Usage

```bash
# Run PDF spider
scrapy crawl fetch_pdf

# Run HTML spider with Splash
scrapy crawl fetch_full_content_cbrands_html_splash

# Run B Corp scraper
python scrapping/scrape_b_corp.py

# Run with output logging
scrapy crawl fetch_pdf -o output.json
```

---

## Output Examples

| Spider | Output File | Format |
|--------|-------------|--------|
| fetch_pdf | `company_content.pdf` | PDF |
| fetch_full_content_cbrands_html_splash | `2023-*.html` | HTML |
| scrape_b_corp | `b_corp_companies.csv` | CSV |

---

## Notes

- Respect `robots.txt` and website terms of service when scraping
- Add appropriate delays between requests to avoid overloading servers
- Some websites may require additional headers or authentication

---

## License

This project is for educational and research purposes.
