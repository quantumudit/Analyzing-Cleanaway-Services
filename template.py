"""
This script generates a standard data science project template
"""

import logging
import os

logging.basicConfig(level=logging.INFO)

list_of_files = [
    "conf/configs.yaml",
    "data/.gitkeep",
    "notebooks/.gitkeep",
    "reports/.gitkeep",
    "src/__init__.py",
    "src/constants.py",
    "src/exception.py",
    "src/logger.py",
    "src/components/.gitkeep",
    "src/pipelines/.gitkeep",
    "src/utils/basic_utils.py",
    "main.py",
    "requirements.txt",
    "setup.py",
    "README.md",
    ".gitignore",
    "LICENSE",
]

# Iterate over file and create them
for file_path in list_of_files:
    file_path = os.path.normpath(file_path)
    file_dir, file_name = os.path.split(file_path)

    # Create directory if not exist
    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info("Creating directory: %s for the file %s", file_dir, file_name)

    # Create file if not exists or if the file is empty
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, "w", encoding="utf-8") as f:
            logging.info("Creating empty files: %s", file_path)

    # Ignore if the non-empty file already exists
    else:
        logging.info("%s already exists", file_name)
