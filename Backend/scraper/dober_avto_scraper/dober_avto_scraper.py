import os
import time
from datetime import datetime
from typing import Any, Dict, List

from Backend.db.MongoConnectionHandler import (
    init_mongo_db_connection,
    close_mongo_db_connection
)
from Backend.db.MongoOperationHandler import insert_data_to_mongo_db
from Backend.logger.log_config import log
from Backend.scraper.utils.api_request_processor import (
    get_json_from_url,
    get_json_from_urls_threaded,
    get_prepared_request_for_get
)
from Backend.scraper.utils.common_helpers import get_end_time
from Backend.scraper.utils.curl_imp_proccessor import curl_threading
from Backend.scraper.utils.decorators import time_it
from Backend.scraper.utils.dir_helper import remove_dir_if_exists_and_create
from Backend.scraper.utils.json_processor import (
    add_datetime_to_list_of_json,
    remove_fields_from_list_of_json
)
from Backend.scraper.utils.lxml_processor import (
    extract_multiple_text_from_html_threaded_with_parser,
    get_files_paths_from_directory
)

# URLS
BASE_URL: str = "https://www.doberavto.si"
BASE_URL_API: str = "https://www.doberavto.si/internal-api/v1/marketplace/search"
BASE_FINANCING_API = "https://www.doberavto.si/internal-api/v1/nlb-widget"

# KEYS TO REMOVE
FIELDS_TO_REMOVE: List[str] = [
    'advertised', 'advertisedTo', 'arrivalStatus', 'badgeFinancing', 
    'badgePromising', 'badgeGoodBuy', 'badgeVerified', 'combinedConsumption',
    'engineDisplacement', 'enginePower', 'externalBadges', 'financing',
    'postingStatus', 'priceType', 'transmission', 'fuelType', 'historySource'
]

# XPATHS
CARS_VIN_XPATH = "//*[contains(@class, 'sub-value') and contains(@class, 'font-bold')]"

# DIRS
CAR_DIRECT_URLS_DIR = "Backend/scraper/dober_avto_scraper/temp"

@time_it
def dober_avto_scraper() -> List[Dict[str, Any]]:
    start = time.time()
    num_of_all_records_int: int = get_number_of_results()

    all_records_url: str = get_all_records_url(num_of_all_records_int)

    all_data_json: Dict[str, Any] = get_all_data(all_records_url)

    all_data_json = all_data_json['results']

    process_json(all_data_json)

    add_all_urls_for_cars(all_data_json)

    add_vin_from_page2(all_data_json)

    remove_non_vin_items_in_list(all_data_json)

    save_to_mongo(all_data_json)

    save_stat(all_data_json, all_data_json, start)


def save_to_mongo(data: Dict[str, Any]):
    db_mongo = None
    try:
        collection_name: str = os.getenv("DOBER_AVTO_PROD_DB")
        db_mongo = init_mongo_db_connection()
        insert_data_to_mongo_db(db_mongo, collection_name, data)
    except Exception as e:
        log.info(f"An error occurred while inserting data to MongoDB: {e}")
    finally:
        pass
        close_mongo_db_connection(db_mongo)


def get_params(fetch_size: int, start: int) -> Dict[str, Any]:
    return {'results': fetch_size, 'from': start, }


def get_number_of_results() -> int:
    params: Dict[str, Any] = get_params(1, 0)
    full_url: str = get_prepared_request_for_get(BASE_URL_API, params)
    data: Dict[str, Any] = get_json_from_url(full_url)
    return data['total']


def get_all_records_url(num_of_records: int) -> str:
    params: Dict[str, Any] = get_params(num_of_records, 0)
    full_url: str = get_prepared_request_for_get(BASE_URL_API, params)
    return full_url


def get_all_data(all_data_url: str) -> Dict[str, Any]:
    data: Dict[str, Any] = get_json_from_url(all_data_url)
    return data


def process_json(data_json: List[Dict[str, Any]]) -> None:
    """Process JSON data by removing unwanted fields and adding metadata."""
    remove_fields_from_list_of_json(data_json, FIELDS_TO_REMOVE)
    add_datetime_to_list_of_json(data_json)
    for item in data_json:
        if isinstance(item, dict) and 'manufacturerName' in item and 'modelName' in item:
            full_name = f"{item['manufacturerName']} {item['modelName']}"
            item['name'] = full_name

def add_all_urls_for_cars(data_json: Dict[str, Any]):
    for item in data_json:
        url = BASE_URL + '/oglas/' + item['postId']
        item['url'] = url

def add_vin_from_page2(data_json: Dict[str, Any]):
    car_direct_urls_list = [f'{BASE_FINANCING_API}/{item["postId"]}' for item in data_json]

    all_json_with_vins = get_json_from_urls_threaded(car_direct_urls_list)
    for item in data_json:
        for data in all_json_with_vins:
            if data and item['postId'] == data['source_url'].split('/')[-1]:
                item['vin'] = data['vehicle_chassis_number']
                break


    car_direct_urls_list = [(item['url'], item['postId']) for item in data_json if not item.get('vin')]

    car_direct_urls_dir = CAR_DIRECT_URLS_DIR
    remove_dir_if_exists_and_create(car_direct_urls_dir)
    curl_threading(car_direct_urls_list, car_direct_urls_dir)

    files_paths = get_files_paths_from_directory(car_direct_urls_dir)

    raw_car_data_with_vins_and_paths_list_of_list = extract_multiple_text_from_html_threaded_with_parser(files_paths, [
        CARS_VIN_XPATH], True)

    for vin, name in raw_car_data_with_vins_and_paths_list_of_list:
        name = name.replace(".html", "").split('/')[-1]
        for item in data_json:
            if item['postId'] == name:
                item['vin'] = vin
                break

def remove_non_vin_items_in_list(data_json: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter out items that don't have a valid VIN number."""
    return [item for item in data_json if 'vin' in item and item['vin']]


def save_stat(total, with_vin, start_time) -> None:
    total = len(total)
    collected = total
    with_vin = len(with_vin)
    time = get_end_time(start_time)

    data = {"source": "doberavto.si", "total": total, "collected": collected, "with_vin": with_vin, "time": time
            , "date_of_insert": datetime.now()}

    db_mongo = None
    try:
        collection_name = os.getenv("SCRAPER_STAT_DB")
        db_mongo = init_mongo_db_connection()
        insert_data_to_mongo_db(db_mongo, collection_name, data)
        log.info("Statistics saved successfully to MongoDB")
    except Exception as e:
        log.error(f"An error occurred while inserting statistics to MongoDB: {e}")
    finally:
        if db_mongo:
            close_mongo_db_connection(db_mongo)

if __name__ == '__main__':
    dober_avto_scraper()