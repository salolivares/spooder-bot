import logging
from tinydb import TinyDB, where, Query


class Database:
    def __init__(self):
        self.db = TinyDB("resources/database.json")
        self.ignoreTable = self.db.table("ignored")
        self.logger = logging.getLogger("spooderBot")
        self.logger.info("Database loaded!")

    def getIgnoredChannels(self):
        return self.ignoreTable.search(where('channels').exists())[0]["channels"]

    def getIgnoredUsers(self):
        return self.ignoreTable.search(where('users').exists())[0]["users"]
