# This is a basic zip extraction script

import zipfile, os

zip_file_path = "path/to/your/zipped/file/resume-dataset.zip"
# zip_file_path = 'path/to/your/file.zip'
extract_to_folder = "path/to/your/extracted/folder"


def extract_zip(zip_file_path, extract_to_folder):
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to_folder)


extract_zip(zip_file_path, extract_to_folder)
