import os
from typing import List

from Backend.db.MongoConnectionHandler import init_mongo_db_connection
from Backend.db.MongoOperationHandler import insert_data_to_mongo_db


def operation05_save_data_db(data: List[List[str]]) -> None:
    try:
        collection_name = os.getenv("AVTO_NET_PROD_DB")
        db_mongo = init_mongo_db_connection()
        insert_data_to_mongo_db(db_mongo, collection_name, data)
    except Exception as e:
        print(f"An error occurred while inserting data to MongoDB: {e}")
    pass