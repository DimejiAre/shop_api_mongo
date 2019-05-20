from pymongo import MongoClient


class Database(object):
    DATABASE = None

    @staticmethod
    def initialize():
        client = MongoClient()
        Database.DATABASE = client.shop

    @staticmethod
    def insert(collection, data):
        return Database.DATABASE[collection].insert(data)

    @staticmethod
    def update_one(collection, query, data):
        return Database.DATABASE[collection].update_one(query, {"$set": data})

    @staticmethod
    def find(collection):
        return Database.DATABASE[collection].find()

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def delete_one(collection, query):
        return Database.DATABASE[collection].delete_one(query)
