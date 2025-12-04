from pymongo import MongoClient

from Backend.logger.log_config import log


class MongoConnectionBuilder:
    def __init__(self):
        self._uri = None
        self._dbname = None
        self._client = None

    def with_uri(self, uri):
        self._uri = uri
        log.info(f"MongoDB URI set to: {uri}")
        return self

    def with_dbname(self, dbname):
        self._dbname = dbname
        log.info(f"MongoDB database name set to: {dbname}")
        return self

    def close_connection(self):
        if self._client:
            self._client.close()
            log.info("MongoDB connection closed.")
        self._client = None

    def get_database(self):
        if not self._client:
            self._client = MongoClient(self._uri)
            log.info("MongoDB connection established.")
        return self._client[self._dbname]

    def build(self):
        if not self._uri:
            log.error("URI must be set before building the connection.")
            raise ValueError("URI must be set")
        if not self._dbname:
            log.error("Database name must be set before building the connection.")
            raise ValueError("Database name must be set")
        return self.get_database()
