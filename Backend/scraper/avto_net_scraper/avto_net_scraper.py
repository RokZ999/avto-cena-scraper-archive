import time
from typing import List

from Backend.scraper.avto_net_scraper.operation01_car_pages_url_collector_v2 import (
    operation01_car_pages_url_collector_v2
)
from Backend.scraper.avto_net_scraper.operation02_car_direct_urls_collector_v2 import (
    operation02_car_direct_urls_collector_v2
)
from Backend.scraper.avto_net_scraper.operation03_car_direct_urls_processor_v2 import (
    operation03_car_direct_urls_processor_v2
)
from Backend.scraper.avto_net_scraper.operation04_car_data_extractor import (
    operation04_car_data_extractor
)
from Backend.scraper.avto_net_scraper.operation05_save_data_db import (
    operation05_save_data_db
)
from Backend.scraper.avto_net_scraper.operation06_stat import operation06_stat


def avto_net_scraper() -> None:
    """Main entry point for avto.net scraper."""
    production()

def sync_production() -> None:
    """Execute the complete scraping pipeline synchronously."""
    start = time.time()

    car_pages_url_list: List[str] = operation01_car_pages_url_collector_v2()
    car_direct_url_list = operation02_car_direct_urls_collector_v2(car_pages_url_list)
    operation03_car_direct_urls_processor_v2(car_direct_url_list)
    all_extract_car_data_dict = operation04_car_data_extractor()
    operation05_save_data_db(all_extract_car_data_dict)
    operation06_stat(car_direct_url_list, all_extract_car_data_dict, start)


def production() -> None:
    """Production wrapper for the scraping pipeline."""
    sync_production()
