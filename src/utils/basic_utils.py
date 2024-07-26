"""
This module provides utility functions for handling files and directories.
It includes functions for reading YAML files, CSV files, creating directories
and writing to CSV files. The functions are designed to handle exceptions and
log relevant information for debugging purposes.
"""

import re
from csv import DictReader, DictWriter
from os import makedirs
from os.path import normpath

import httpx
import yaml
from box import Box
from rich.table import Table

from src.exception import CustomException
from src.logger import logger


def read_yaml(yaml_path: str) -> Box:
    """
    This function reads a YAML file from the provided path and returns
    its content as a Box object.

    Args:
        yaml_path (str): The path to the YAML file to be read.

    Raises:
        CustomException: If there is any error while reading the file or
        loading its content, a CustomException is raised with the original
        exception as its argument.

    Returns:
        Box: The content of the YAML file, loaded into a Box object for
        easy access and manipulation.
    """
    try:
        yaml_path = normpath(yaml_path)
        with open(yaml_path, "r", encoding="utf-8") as yf:
            content = Box(yaml.safe_load(yf))
            logger.info("yaml file: %s loaded successfully", yaml_path)
            return content
    except Exception as e:
        logger.error(CustomException(e))
        raise CustomException(e) from e


def create_directories(dir_paths: list, verbose=True) -> None:
    """
    This function creates directories at the specified paths.

    Args:
        dir_paths (list): A list of directory paths where directories need
        to be created.
        verbose (bool, optional): If set to True, the function will log
        a message for each directory it creates. Defaults to True.
    """
    for path in dir_paths:
        makedirs(normpath(path), exist_ok=True)
        if verbose:
            logger.info("created directory at: %s", path)


def write_to_csv(csv_filepath: str, data: dict, verbose: bool = False) -> None:
    """
    This function writes a dictionary to a CSV file. If the file
    does not exist, it will be created.

    Args:
        csv_filepath (str): The path to the CSV file to which the data
            should be written.
        data (dict): The data to be written to the CSV file. The keys of the
            dictionary are used as field names.
        verbose (bool, optional): If True, the function will log the data
            that was written to the CSV file. Defaults to False.

    Raises:
        CustomException: If there is an error while writing to the CSV file,
        a CustomException will be raised with the original exception
        as its argument.
    """
    try:
        csv_path = normpath(csv_filepath)

        # Write to the file (This will create the CSV file if not exists)
        with open(csv_path, "a", newline="", encoding="utf-8") as cf:
            writer = DictWriter(cf, fieldnames=data.keys())

            # Write the headers (only for the first time)
            if cf.tell() == 0:
                writer.writeheader()
                logger.info("CSV file: %s created successfully", csv_path)

            # Write the new data rows
            writer.writerow(data)

            if verbose:
                logger.info("1 row added: %s", data)
    except Exception as e:
        logger.error(CustomException(e))
        raise CustomException(e) from e


def read_csv(csv_filepath: str, delimiter: str = ",") -> list:
    """
    This function reads a CSV file and returns its content as a list of
    dictionaries. Each dictionary represents a row in the CSV file with
    keys as column names and values as row values.

    Args:
        csv_filepath (str): The path to the CSV file to be read.
        delimiter (str, optional): The character used to separate values
        in the CSV file. Defaults to ",".

    Raises:
        CustomException: If there is an error in opening or reading the
        CSV file, a CustomException is raised with the original exception
        as its argument.

    Returns:
        list: A list of dictionaries representing the content of the CSV file.
    """
    try:
        csv_path = normpath(csv_filepath)
        with open(csv_path, "r", encoding="utf-8") as cf:
            reader = DictReader(cf, delimiter=delimiter)
            logger.info("CSV file: %s loaded successfully", csv_path)
            return list(reader)
    except Exception as e:
        logger.error(CustomException(e))
        raise CustomException(e) from e


def dict_to_table(data: dict, title: str):
    # Create a table
    table = Table(title=title)

    # Add columns
    table.add_column(
        "Dataframe Attributes", justify="left", style="bright_cyan", no_wrap=True
    )
    table.add_column("Value", justify="right", style="bright_magenta")

    # Add rows
    for key, value in data.items():
        table.add_row(key, str(value))
    return table


def get_lat_long(address):
    url = f"https://nominatim.openstreetmap.org/?q={address}&format=json"
    response = httpx.get(url)
    if response.status_code == 200:
        data = response.json()
        return {"lat": float(data[0]["lat"]), "long": float(data[0]["lon"])}
    else:
        return "Error: Unable to retrieve location information"


def get_postcode(address):
    postcode_pattern = r".* (\d{4})"
    url = f"https://nominatim.openstreetmap.org/?q={address}&format=json"
    response = httpx.get(url)
    if response.status_code == 200:
        data = response.json()
        for loc in data:
            loc_name = loc["display_name"]
            if re.findall(postcode_pattern, loc_name):
                return re.findall(postcode_pattern, loc_name)
    else:
        return "Error: Unable to retrieve location information"
