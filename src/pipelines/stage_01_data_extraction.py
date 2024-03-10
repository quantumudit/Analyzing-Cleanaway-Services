"""
This module is responsible for the data extraction pipeline,
which includes product link extraction and product info scraping.
"""

from src.components.link_extractor import LinkExtractor

# from src.components.service_scraper import ServicesInfoScraper
from src.exception import CustomException
from src.logger import logger


class DataExtractionPipeline:
    """
    This class represents the data extraction pipeline.
    It includes methods for product link extraction and product info scraping.
    """

    def __init__(self):
        pass

    def main(self):
        """
        This method is the main execution point for the data extraction
        pipeline. It first extracts product links and then scrapes
        product info.

        Raises:
            CustomException: If any error occurs during the data extraction
            process, a CustomException is raised.
        """
        try:
            logger.info("Services link extraction started")
            link_extractor = LinkExtractor()
            link_extractor.scrape_service_links()
            logger.info("Services link extraction completed successfully")
            # logger.info("Services info extraction started")
            # product_scraper = ServicesInfoScraper()
            # product_scraper.scrape_servicess()
            # logger.info("Services info extraction completed successfully")
        except Exception as excp:
            logger.error(CustomException(excp))
            raise CustomException(excp) from excp


if __name__ == "__main__":
    STAGE_NAME = "Data Extraction Stage"

    try:
        logger.info(">>>>>> %s started <<<<<<", STAGE_NAME)
        obj = DataExtractionPipeline()
        obj.main()
        logger.info(">>>>>> %s completed <<<<<<\n\nx==========x", STAGE_NAME)
    except Exception as e:
        logger.error(CustomException(e))
        raise CustomException(e) from e
