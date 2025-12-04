from Backend.logger.log_config import log


def insert_data_to_mongo_db(db_mongo, collection_name: str, data_json):
    try:
        collection = db_mongo[collection_name]
        log.info(f"Inserting data into MongoDB collection '{collection_name}'")

        if isinstance(data_json, list):
            result = collection.insert_many(data_json)
            log.info(f"Inserted {len(result.inserted_ids)} documents into '{collection_name}' collection.")
            return {"success": True, "inserted_ids": result.inserted_ids}
        elif isinstance(data_json, dict):
            result = collection.insert_one(data_json)
            log.info(f"Inserted a document with ID {result.inserted_id} into '{collection_name}' collection.")
            return {"success": True, "inserted_id": result.inserted_id}
        else:
            log.error("Data to insert must be a dictionary or a list of dictionaries.")
            raise ValueError("data_json must be a dictionary or a list of dictionaries")
    except Exception as e:
        log.error(f"Failed to insert data into '{collection_name}' collection: {e}")
        return {"success": False, "error": str(e)}
