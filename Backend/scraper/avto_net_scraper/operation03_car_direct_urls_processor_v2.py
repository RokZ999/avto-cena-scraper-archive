import re
from typing import List

from Backend.scraper.avto_net_scraper.common.common_constants import OPERATION03_CAR_DIRECT_URLS_DIR, TEMP_DIR
from Backend.scraper.utils.curl_imp_proccessor import curl_threading
from Backend.scraper.utils.dir_helper import remove_dir_if_exists_and_create
from Backend.scraper.utils.lxml_processor import get_files_paths_from_directory, extract_text_from_html

# XPATHS
CARS_XPATH = "//th[contains(., 'VIN / številka šasije:')]/following-sibling::td"
# SYSTEM PATHS
car_direct_urls_dir = OPERATION03_CAR_DIRECT_URLS_DIR


def operation03_car_direct_urls_processor_v2(car_direct_urls_list: List[str]) -> None:
    remove_dir_if_exists_and_create(car_direct_urls_dir)
    url_file_name_tuple_list = generate_url_file_name_tuple_list(car_direct_urls_list)
    curl_threading(url_file_name_tuple_list, car_direct_urls_dir)



def generate_url_file_name_tuple_list(urls: List[str]):
    return [(url, extract_id_from_avto_net_url(url)) for url in urls]


def extract_id_from_avto_net_url(url):
    pattern = r"id=(\d+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None
