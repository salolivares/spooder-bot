import logging
from tinydb import TinyDB


class Database:
    def __init__(self):
        self.db = TinyDB("resources/db.json")
        self.logger = logging.getLogger("spooderBot")
        self.logger.info("Database loaded!")

    def insert(self, data: dict):
        self.db.insert(data)