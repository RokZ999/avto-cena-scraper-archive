import os
import re
from typing import List

from Backend.scraper.avto_net_scraper.common.common_constants import TEMP_DIR, OPERATION03_CAR_DIRECT_URLS_DIR
from Backend.scraper.utils.dir_helper import save_file
from Backend.scraper.utils.json_processor import add_datetime_to_list_of_json
from Backend.scraper.utils.lxml_processor import get_files_paths_from_directory, \
    extract_multiple_text_from_html_threaded_with_parser, extract_multiple_text_from_html_threaded_with_parser_v2

car_direct_urls_dir = OPERATION03_CAR_DIRECT_URLS_DIR

# XPaths
CARS_VIN_XPATH = "//th[contains(.,'VIN /')]/following-sibling::td"
NAME_PART1_XPATH = "(//h3)[1]"
CARS_PRICE_XPATH = "//p[@class='h1 font-weight-bold align-middle pt-3']"
MOBILE_NUM_XPATH = "(//a[contains(@href, 'tel:')])[1]"
ODOMOTER_XPATH = "//th[contains(.,'Prevoženi km')]/following-sibling::td"
YEAR_XPATH = "//th[contains(.,'Prva registracija')]/following-sibling::td"

ALL_XPATH_LIST = [CARS_VIN_XPATH, NAME_PART1_XPATH, CARS_PRICE_XPATH, MOBILE_NUM_XPATH, ODOMOTER_XPATH, YEAR_XPATH]


def operation04_car_data_extractor():
    save_to_cache = os.getenv("SAVE_TXT")

    all_cars_paths_with_vins_list = get_all_paths_with_vins()
    all_car_data_list_of_list = get_all_car_data(all_cars_paths_with_vins_list)

    if save_to_cache == 'True':
        save_file(all_car_data_list_of_list, f"{TEMP_DIR}/all.txt")

    all_car_data_list_of_dicts = clean_and_convert_data_to_dict(all_car_data_list_of_list)
    add_datetime_to_list_of_json(all_car_data_list_of_dicts)

    return all_car_data_list_of_dicts


def get_all_paths_with_vins() -> List[List[str]]:
    files_paths = get_files_paths_from_directory(car_direct_urls_dir)
    raw_car_data_with_vins_and_paths_list_of_list = extract_multiple_text_from_html_threaded_with_parser(
        files_paths,
        [CARS_VIN_XPATH],
        True
    )
    only_vin_path_list_of_list = [car_data for car_data in raw_car_data_with_vins_and_paths_list_of_list if
                                  car_data[0] != '']
    all_cars_paths_with_vins_list = [car_data[1] for car_data in only_vin_path_list_of_list]
    return all_cars_paths_with_vins_list


def get_all_car_data(file_paths):
    return extract_multiple_text_from_html_threaded_with_parser_v2(file_paths, ALL_XPATH_LIST, True)


def clean_and_convert_data_to_dict(raw_car_data: List[List[str]]):
    result = []
    for car_data in raw_car_data:
        if len(car_data) > 2 and "€" in car_data[2]:
            print(car_data)
            car_dict = {
                'vin': car_data[0],
                'name': car_data[1],
                'price': int(car_data[2].replace('€', '').replace('.', '').strip()),
                'contactPersonPhone': car_data[3],
                'odometer': int(car_data[4].strip()) if car_data[4] else -1,
                'registrationDate': re.sub(r'\s', '', car_data[5]) if car_data[5] else '',
                'url': "https://avto.net/Ads/details.asp?id=" + car_data[6].split('/')[-1].replace(".html", "")
            }
            result.append(car_dict)
    return result
