"""
This module is responsible for executing the data extraction and data
preprocessing stages of a data pipeline.

It imports and uses the DataExtractionPipeline and DataPreprocessingPipeline
classes from the src.pipelines package.

Each stage is wrapped in a try-except block to handle and log any
exceptions that may occur during the execution of the stages.

The logger from the src.logger module is used for logging the start and
completion of each stage, as well as any exceptions that may occur.
"""

from src.exception import CustomException
from src.logger import logger
# from src.pipelines.stage_01_data_extraction import DataExtractionPipeline
from src.pipelines.stage_02_data_transformation import DataTransformationPipeline

# STAGE_NAME = "Data Extraction Stage"

# try:
#     logger.info(">>>>>> %s started <<<<<<", STAGE_NAME)
#     obj = DataExtractionPipeline()
#     obj.main()
#     logger.info(">>>>>> %s completed <<<<<<\n\nx==========x", STAGE_NAME)
# except Exception as e:
#     logger.error(CustomException(e))
#     raise CustomException(e) from e


STAGE_NAME = "Data Transformation Stage"

try:
    logger.info(">>>>>> %s started <<<<<<", STAGE_NAME)
    obj = DataTransformationPipeline()
    obj.main()
    logger.info(">>>>>> %s completed <<<<<<\n\nx==========x", STAGE_NAME)
except Exception as e:
    logger.error(CustomException(e))
    raise CustomException(e) from e
