import os
import shutil

from Backend.logger.log_config import log


def remove_dir_if_exists_and_create(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)

def save_file(content, file_path_with_name):
    with open(file_path_with_name, "w", encoding='utf-8') as file:
        for line in content:
            if isinstance(line, list):
                file.write(', '.join(line).replace('\xa0', ' ') + "\n")
            else:
                file.write(line.replace('\xa0', ' ') + "\n")

def read_file(file_path_with_name):
    if not os.path.exists(file_path_with_name):
        log.error(f"File {file_path_with_name} does not exist.")
        return []
    with open(file_path_with_name, "r") as file:
        return [line.strip() for line in file.readlines()]