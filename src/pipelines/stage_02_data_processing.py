"""
This module is responsible for the data extraction pipeline,
which includes product link extraction and product info scraping.
"""

from src.components.data_processor import DataProcessor
from src.exception import CustomException
from src.logger import logger


class DataProcessingPipeline:
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
            logger.info("Data transformation started")
            data_processor = DataProcessor()
            data_processor.data_transformation()
            logger.info("Data transformation completed successfully")
        except Exception as excp:
            logger.error(CustomException(excp))
            raise CustomException(excp) from excp


if __name__ == "__main__":
    STAGE_NAME = "Data Processing Stage"

    try:
        logger.info(">>>>>> %s started <<<<<<", STAGE_NAME)
        obj = DataProcessingPipeline()
        obj.main()
        logger.info(">>>>>> %s completed <<<<<<\n\nx==========x", STAGE_NAME)
    except Exception as e:
        logger.error(CustomException(e))
        raise CustomException(e) from e
