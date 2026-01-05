import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urlparse


class FetchContentSpiderCBrandsHtml(scrapy.Spider):
    name = 'fetch_full_content_cbrands_html_splash'

    def __init__(self, *args, **kwargs):
        super(FetchContentSpiderCBrandsHtml, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.cbrands.com/']
        self.visited_urls = set()  # To avoid revisiting URLs
        self.file_counter = 0  # Counter to generate sequential filenames

    def start_requests(self):
        """Initiate requests using SplashRequest."""
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
                endpoint='render.html',  # Use Splash's render.html endpoint
                args={'wait': 2},  # Add a wait time for JS to load
            )

    def parse(self, response):
        try:
            self.log(f"Processing URL: {response.url}")

            # Extract visible text while excluding unnecessary tags (script, style, etc.)
            all_text = response.xpath(
                "//body//*[not(self::script or self::style or self::noscript or self::iframe or self::code or self::pre or self::nav or self::header or self::footer)]//text()"
            ).getall()

            # Filter out repetitive or irrelevant content
            raw_text_blocks = [
                text.strip() for text in all_text if text.strip()
                and not any(kw in text.lower() for kw in [
                    'our story', 'featured', 'overview', 'search', 'privacy notice', 'facebook',
                    'instagram', 'linkedin', 'careers', 'job opportunities', 'applicant privacy',
                    'terms and conditions', 'top',
                    'do not sell', 'contact', 'newsroom', 'brand center', 'terms of use', 'privacy policy', 'cookie policy'
                ])
            ]

            if not raw_text_blocks:
                self.log(f"No meaningful content found on the page: {response.url}")
                return

            # Log the extracted content for debugging purposes
            with open("debug_content.txt", "w", encoding="utf-8") as debug_file:
                debug_file.write(f"URL: {response.url}\n\n")
                debug_file.write("\n".join(raw_text_blocks))

            # Format the content with individual blocks separated into <p> tags
            formatted_content = f"<html><head><title>Content from {response.url}</title></head><body>"
            formatted_content += f"<h1>Content from {response.url}</h1>\n"
            formatted_content += "\n".join([f"<p>{block}</p>" for block in raw_text_blocks])
            formatted_content += "</body></html>"

            # Generate a sequential HTML file name
            self.file_counter += 1
            file_name = f"2023-{self.file_counter}.html"
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(formatted_content)

            self.log(f"Saved content as HTML: {file_name}")

            # Follow internal and relevant external links
            self.visited_urls.add(response.url)  # Mark current URL as visited
            for link in response.xpath("//a/@href").getall():
                absolute_url = response.urljoin(link)
                if absolute_url not in self.visited_urls:
                    if (self.is_internal_link(absolute_url) or self.is_relevant_external_link(absolute_url)) and not self.is_excluded_link(absolute_url):
                        yield SplashRequest(
                            url=absolute_url,
                            callback=self.parse,
                            endpoint='render.html',
                            args={'wait': 2},
                        )

        except Exception as e:
            self.log(f"An error occurred while processing {response.url}: {e}")

    @staticmethod
    def is_internal_link(url):
        """Check if a URL is an internal link."""
        main_domain = "cbrands.com"
        return main_domain in urlparse(url).netloc

    @staticmethod
    def is_relevant_external_link(url):
        """Check if a URL is a relevant external link."""
        # Define keywords or patterns that identify relevant external links
        relevant_keywords = ["cbrands"]
        domain = urlparse(url).netloc.lower()
        return any(keyword in domain or keyword in url.lower() for keyword in relevant_keywords)

    @staticmethod
    def is_excluded_link(url):
        """Check if a URL should be excluded."""
        excluded_keywords = ["careers", "jobs", "product-locator", "contact", "buy", "spiritofcbrands"]
        return any(keyword in url.lower() for keyword in excluded_keywords)
