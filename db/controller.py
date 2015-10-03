__author__ = 'HoonKim'

from pymongo import MongoClient


class Mongo:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)

    @staticmethod
    def get_server(token):
        return token

    def push(self, url, body, token) :
        server = self.get_server(token)
        if server is not None :
            db = self.client[server]
        else :
            return False

        collection_name = url[-1]
        collection = db[collection_name]
        collection.insert(body)

        return True


