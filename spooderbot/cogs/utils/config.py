from .fileIO import fileIO
import discord
import os

default_path = "data/spooderbot/config.json"
default_config = {
    "owner": "140350353521639424",
    "admins": [
        "140208896726925312"
    ],
    "mods": [],
    "roles": []
}


class Config:
    def __init__(self, path=default_path):
        self.path = path
        self.check_folders()

        if not fileIO.is_valid_json(self.path):
            self.bot_config = default_config
            self.save_config()
        else:
            current = fileIO.load_json(self.path)
            if current.keys() != default_config.keys():
                for key in default_config.keys():
                    if key not in current.keys():
                        current[key] = default_config[key]
                        print("Adding " + str(key) + " field to spooderbot config.json")
                fileIO.save_json(self.path, current)
            self.bot_config = fileIO.load_json(self.path)

    def check_folders(self):
        folders = ("data", os.path.dirname(self.path), "cogs", "cogs/utils")
        for folder in folders:
            if not os.path.exists(folder):
                print("Creating " + folder + " folder...")
                os.makedirs(folder)

    def save_config(self):
        fileIO.save_json(self.path, self.bot_config)

    @property
    def owner(self):
        return self.bot_config["owner"]

    @owner.setter
    def owner(self, value):
        self.bot_config["owner"] = value
        self.save_config()

    @property
    def admins(self):
        return self.bot_config["admins"]

    @admins.setter
    def admins(self, value):
        self.bot_config["admins"] = value
        self.save_config()

    @property
    def mods(self):
        return self.bot_config["mods"]

    @mods.setter
    def mods(self, value):
        self.bot_config["mods"] = value
        self.save_config()

    @property
    def roles(self):
        return self.bot_config["roles"]

    @roles.setter
    def roles(self, value):
        self.bot_config["roles"] = value
        self.save_config()