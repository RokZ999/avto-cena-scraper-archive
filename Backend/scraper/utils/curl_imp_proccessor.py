from typing import List, Tuple
import os
import subprocess
import time


from Backend.logger.log_config import log
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_curl_imp_path_in_project():
    curl_imp_os = os.getenv('CURL_IMP_OS')
    if curl_imp_os == 'linux':
        return "Backend/scraper/utils/curlimp/ubuntu_linux"
    elif curl_imp_os == 'win':
        return "Backend/scraper/utils/curlimp/windows"
    else:
        log.error(f"The system os is not defined correctly, curl_imp_os='{curl_imp_os}'")

def build_curl_command_with_output_to_save(file_name, url, dir_to_save):
    dir_base = "../../../../.."
    curl_imp_os = os.getenv('CURL_IMP_OS')
    if curl_imp_os == 'linux':
        return [
            "./curl_chrome116",
            "--url", url,
            "--output", f"{dir_base}/{dir_to_save}/{file_name}.html"
        ]
    elif curl_imp_os == 'win':
        return [
            "curl_chrome116.bat",
            "--url", f'"{url}"'
            " --output", f'"{dir_base}/{dir_to_save}/{file_name}.html"'
        ]
    else:
        log.error(f"The system os is not defined correctly, curl_imp_os='{curl_imp_os}'")

def execute_curl(command):
    url_index = command.index("--url") + 1
    url = command[url_index] if url_index < len(command) else "Unknown URL"

    curl_imp_os = os.getenv('CURL_IMP_OS')
    if curl_imp_os == 'linux':
        #time.sleep(0.5)
        result = subprocess.run(command, capture_output=True, text=True)
    if curl_imp_os == 'win':
        command_str = ' '.join(command)
        result = subprocess.run(command_str, capture_output=True, text=True)

    if result.returncode != 0:
        log.error(f"Error executing curl for URL {url}: {result.stderr}")
        return 0
    else:
        log.info(f"Command for URL {url} executed successfully.")
        return 1

from concurrent.futures import ThreadPoolExecutor
def curl_threading(url_file_name_tuple_list: List[Tuple[str, str]], dir_to_save: str):
    original_dir = os.getcwd()
    os.chdir(get_curl_imp_path_in_project())
    success_count = 0
    num_of_workers = int(os.getenv("THREAD_COUNT"))
    with ThreadPoolExecutor(max_workers=num_of_workers) as executor:
        futures = [executor.submit(execute_curl, build_curl_command_with_output_to_save(file_name, url, dir_to_save)) for url, file_name in url_file_name_tuple_list]
        for future in futures:
            success_count += future.result()
    os.chdir(original_dir)
    failure_count = len(url_file_name_tuple_list) - success_count
    log.info(f"Total successful executions: {success_count}")
    log.info(f"Total failed executions: {failure_count}")