import scrapy
import pdfkit


class FetchPDFSpider(scrapy.Spider):
    name = 'fetch_pdf'

    def __init__(self, *args, **kwargs):
        super(FetchPDFSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.gallo.com/']

    def parse(self, response):
        try:
            self.log(f"Processing URL: {response.url}")

            # Extract all visible text from the website
            all_text = response.xpath("//body//*[not(self::script or self::style)]//text()").getall()
            raw_text = "\n".join([text.strip() for text in all_text if text.strip()])

            if not raw_text:
                self.log(f"No content found on the page: {response.url}")
                return

            # Filter content related to company
            keyword = "Gallo"
            twe_related_content = [
                text for text in raw_text.split("\n") if keyword.lower() in text.lower()
            ]

            if not twe_related_content:
                self.log(f"No content found related to {keyword} on {response.url}")
                return

            # Format and save the content as a PDF
            formatted_text = "\n".join(twe_related_content)
            formatted_content = f"<h1>Information from {response.url}</h1>\n<p>{formatted_text}</p>"

            # Generate a unique PDF file
            file_name = f"company_content.pdf"
            pdfkit.from_string(formatted_content, file_name)

            self.log(f"Saved company-related content as PDF: {file_name}")
        except Exception as e:
            self.log(f"An error occurred while processing {response.url}: {e}")
