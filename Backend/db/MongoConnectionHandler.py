import os

from Backend.db.MongoConnectionBuilder import MongoConnectionBuilder
from Backend.logger.log_config import log


def init_mongo_db_connection() -> MongoConnectionBuilder:
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")

    db_mongo_builder = (MongoConnectionBuilder()
                        .with_uri(mongo_uri)
                        .with_dbname(db_name))

    db_mongo = db_mongo_builder.build()
    return db_mongo


def close_mongo_db_connection(db_mongo: MongoConnectionBuilder) -> None:
    if is_mongo_db_connection_initialized(db_mongo):
        db_mongo.client.close()
        log.info("MongoDB connection closed successfully.")


def is_mongo_db_connection_initialized(db_mongo: MongoConnectionBuilder) -> bool:
    if db_mongo is not None:
        return True
    else:
        log.error("MongoDB connection builder is not initialized.")
        raise ValueError("MongoDB connection builder is not initialized.")
