from datetime import datetime
import os

from Backend.db.MongoConnectionHandler import init_mongo_db_connection
from Backend.db.MongoOperationHandler import insert_data_to_mongo_db
from Backend.scraper.avto_net_scraper.common.common_constants import OPERATION03_CAR_DIRECT_URLS_DIR
from Backend.scraper.utils.common_helpers import get_end_time
from Backend.scraper.utils.lxml_processor import get_files_paths_from_directory

car_direct_urls_dir = OPERATION03_CAR_DIRECT_URLS_DIR


def operation06_stat(total, with_vin, start_time) -> None:
    total = len(total)
    collected = len(get_files_paths_from_directory(car_direct_urls_dir))
    with_vin = len(with_vin)
    time = get_end_time(start_time)

    data = {"source": "avto.net", "total": total, "collected": collected, "with_vin": with_vin, "time": time
            , "date_of_insert": datetime.now()}

    try:
        collection_name = os.getenv("SCRAPER_STAT_DB")
        db_mongo = init_mongo_db_connection()
        insert_data_to_mongo_db(db_mongo, collection_name, data)
    except Exception as e:
        print(f"An error occurred while inserting data to MongoDB: {e}")
    pass
