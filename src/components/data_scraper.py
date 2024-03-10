"""
This module contains the ProductInfoScraper class, which is used for scraping
product information from websites. It uses HTTP requests to retrieve the
HTML content of product pages, and then uses the selectolax library to
parse the HTML and extract the desired information. The scraped data is then
stored in a CSV file.
"""

import random
import re
import time
from dataclasses import asdict
from datetime import datetime
from os.path import exists, normpath

import httpx
from selectolax.parser import HTMLParser

from src.constants import CONFIGS, ServiceInfo
from src.exception import CustomException
from src.logger import logger
from src.utils.basic_utils import read_csv, read_yaml, write_to_csv


class DataScraper:
    """
    The ProductInfoScraper class is responsible for scraping product
    information from websites. It provides methods for retrieving product
    details from a given URL, as well as for scraping multiple products
    from a list of URLs. The class uses various libraries and modules, such
    as httpx, fake_useragent, and selectolax, to perform the scraping tasks.
    The scraped data is stored in a CSV file.
    """

    def __init__(self):
        # Read the configuration files
        self.configs = read_yaml(CONFIGS).data_scraper

        # Inputs
        self.user_agent = self.configs.user_agent
        self.timeout = self.configs.timeout
        self.clear = self.configs.clear_contents
        self.links_data_path = normpath(self.configs.links_data_path)

        # Output file paths
        self.scraped_data_path = normpath(self.configs.scraped_data_path)

        # Clear the files if exists
        if self.clear:
            if exists(self.scraped_data_path):
                with open(self.scraped_data_path, "w", encoding="utf-8") as f:
                    f.truncate()
                logger.info("Cleared existing contents from %s", self.scraped_data_path)

    def get_service_details(self, svc_url: str, svc_nm_crd: str, svc_adrs_crd: str):
        """
        Fetches and parses the product details from a given product URL.

        Args:
            product_url (str): The URL of the product to be scraped.
            headers (str): The headers to be used in the HTTP request.

        Raises:
            CustomException: If there is an error during the HTTP request
            or parsing the response.

        Returns:
            None: Writes the scraped product details to a CSV file.
        """
        headers = {"User-Agent": self.user_agent, "accept-language": "en-US"}
        response = httpx.get(svc_url, headers=headers, timeout=self.timeout)
        try:
            logger.info(
                "Request responded with the status code: %s", response.status_code
            )

            # Parse the HTML content
            html = HTMLParser(response.text)

            # CSS selectors
            service_name_css = "div.location-box h1"
            address_css = "div.location-box div.info-block:first-of-type p a"
            last_info_block = "div.location-box div.info-block:last-of-type"
            services_title_css = f"{last_info_block} div.info-block__title"
            services_offered_css = f"{last_info_block} div.info-block__desc p"

            def fetch(selector, output="text"):
                if html.css_first(selector):
                    if output == "text":
                        output = html.css_first(selector).text(strip=True)
                    elif output == "link":
                        output = html.css_first(selector).attrs["href"]
                else:
                    output = None
                return output

            # Service and service address
            service_name = (
                svc_nm_crd
                if fetch(service_name_css) is None
                else fetch(service_name_css)
            )
            service_address = (
                svc_adrs_crd if fetch(address_css) is None else fetch(address_css)
            )

            # Address URL
            address_url = fetch(address_css, "link")

            # RegEx pattern match for latitude and longitudes
            if address_url:
                lat_long_pattern = re.compile(r".*\?q=(.*)\,(.*)")
                matches = lat_long_pattern.match(address_url)
                lat, long = matches.group(1), matches.group(2)
            else:
                lat, long = None, None

            # Services offered
            if fetch(services_offered_css):
                services_offered = (
                    fetch(services_offered_css)
                    if "Services" in fetch(services_title_css)
                    else "Miscellaneous"
                )
            else:
                services_offered = None

            # Get the product details in data class
            service_details = ServiceInfo(
                service_name=service_name,
                address=service_address,
                latitude=lat,
                longitude=long,
                services_offered=services_offered,
                details_url=svc_url,
                scrape_ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            # Write scraped info into CSV file
            write_to_csv(self.scraped_data_path, asdict(service_details))

        except Exception as e:
            logger.error(CustomException(e))
            raise CustomException(e) from e

    def scrape_services(self) -> None:
        """
        Reads a CSV file with product URLs and scrapes each product's details.

        The function generates random headers and sleep times between requests
        to avoid being blocked by the server. The scraped product details are
        written to a CSV file. The function logs the start and end time of the
        scraping process, as well as the total time taken.

        Returns:
            None
        """
        # Read the CSV file with product links
        service_links = read_csv(self.links_data_path)

        # Scraping start time
        start_time = time.time()

        # Start scraping product in loop
        logger.info("Services scraping started")
        for idx, link in enumerate(service_links):
            service_url = link["service_url"]
            service_name_card = link["service_name"]
            service_address_card = link["service_address"]

            # Generate random sleep time
            sleep_sec = random.randint(1, 3)

            # write services data to csv file
            self.get_service_details(
                service_url, service_name_card, service_address_card
            )
            logger.info("%s services detail scraped", idx + 1)
            time.sleep(sleep_sec)

        # Scraping end time
        end_time = time.time()

        # Scraping time interval
        time_diff = round(end_time - start_time)

        # Log time taken for scraping
        logger.info("Time taken for scraping: %s seconds", f"{time_diff:.2f}")
        logger.info("All services url scraped")
