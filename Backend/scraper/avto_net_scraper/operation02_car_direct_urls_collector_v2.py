import os
import random
from typing import List

from Backend.logger.log_config import log
from Backend.scraper.avto_net_scraper.common.common_constants import BASE_URL, OPERATION02_CAR_PAGES_DIR, \
    CAR_DIRECT_URLS
from Backend.scraper.utils.curl_imp_proccessor import curl_threading
from Backend.scraper.utils.decorators import time_it
from Backend.scraper.utils.dir_helper import remove_dir_if_exists_and_create, read_file, save_file
from Backend.scraper.utils.lxml_processor import get_files_paths_from_directory, extract_direct_links, \
    extract_text_from_html
    
# XPATHS
CARS_XPATH = "//a[@class='stretched-link']"
# SYSTEM PATHS
car_pages_dir = OPERATION02_CAR_PAGES_DIR
car_direct_urls = CAR_DIRECT_URLS


def operation02_car_direct_urls_collector_v2(car_pages_urls) -> List[str]:
    save_to_cache = os.getenv("SAVE_TXT")
    use_cache = os.getenv("USE_TXT")

    if use_cache == 'True':
        return read_file(car_direct_urls)
    else:
        remove_dir_if_exists_and_create(car_pages_dir)
        url_file_name_tuple_list = generate_url_file_name_tuple_list(car_pages_urls)
        curl_threading(url_file_name_tuple_list, car_pages_dir)
        log.info("Done collecting car URLs.")
        un_modified_urls = get_all_direct_links_to_cars_from_downloaded_htmls()
        processed_urls = [extract_url(url).replace("..", BASE_URL) for url in un_modified_urls]

        if save_to_cache == 'True':
            save_file(processed_urls, car_direct_urls)

        return processed_urls


def generate_url_file_name_tuple_list(urls: List[str]):
    return [(url, i) for i, url in enumerate(urls)]

def extract_url(url):
    first_occurrence = url.find('&display')
    return url[:first_occurrence]


def get_all_direct_links_to_cars_from_downloaded_htmls() -> List[str]:
    files_paths = get_files_paths_from_directory(car_pages_dir)
    hrefs = extract_direct_links(files_paths, CARS_XPATH)
    return hrefs
