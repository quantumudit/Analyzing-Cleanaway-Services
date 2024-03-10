"""
This module is used to setup a Python package for distribution. It includes
the package metadata such as name, version, author details, description, and
project URLs. It also includes a function to read and filter the requirements
from a file. The setup function from setuptools is used to package the code.
"""

from setuptools import find_packages, setup

IGNORE_ITEMS = ["-e .", "-i https://pypi.org/simple", ""]

__VERSION__ = "0.0.0"
REPO_NAME = "Analyzing-Pokemons"
SRC_REPO = "src"
AUTHOR_NAME = "Udit Kumar Chatterjee"
AUTHOR_EMAIL = "quantumudit@gmail.com"
AUTHOR_GH_USERNAME = "quantumudit"
SHORT_DESCRIPTION = "A python package for scraping and analyzing Pokémons"
GH_URL = "https://github.com/"

with open("README.md", encoding="utf-8") as readme:
    LONG_DESCRIPTION = readme.read()


def get_requirements(file_path: str) -> list[str]:
    """
    This function reads a file from the provided file path, strips
    each line, and filters out any items in the IGNORE_ITEMS list.

    Args:
        file_path (str): The path to the file that contains the requirements.

    Returns:
        list[str]: A list of requirements that are not in the
        IGNORE_ITEMS list.
    """
    with open(file_path, encoding="utf-8") as f:
        contents = [item.strip() for item in f.readlines()]
        requirements = [item for item in contents if item not in IGNORE_ITEMS]
        return requirements


setup(
    name=SRC_REPO,
    version=__VERSION__,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content="text/markdown",
    url=f"{GH_URL}/{AUTHOR_GH_USERNAME}/{REPO_NAME}",
    project_urls={"Bug Tracker": f"{GH_URL}/{AUTHOR_GH_USERNAME}/{REPO_NAME}/issues"},
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=get_requirements("./requirements.txt"),
)
