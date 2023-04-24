import os
from pymongo import MongoClient

MONGO_URL = os.getenv('MONGO_URL', 'test')
MONGO_DB = os.getenv('MONGO_DB', 'test')


class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]

    def _convert_doc(self, doc):
        doc['_id'] = str(doc['_id'])
        return doc

    def find_one(self, collection, query):
        result = self.db[collection].find_one(query)
        if result:
            result = self._convert_doc(result)
        return result

    def find_many(self, collection, query):
        results = self.db[collection].find()
        return [self._convert_doc(doc) for doc in results]

    def insert_one(self, collection, doc):
        result = self.db[collection].insert_one(doc)
        return str(result.inserted_id)

    def insert_many(self, collection, docs):
        result = self.db[collection].insert_many(docs)
        return [str(id) for id in result.inserted_ids]

    def update_one(self, collection, filter, update):
        result = self.db[collection].update_one(filter, update)
        return {
            'matched_count': result.matched_count,
            'modified_count': result.modified_count,
        }

    def update_many(self, collection, filter, update):
        result = self.db[collection].update_many(filter, update)
        return {
            'matched_count': result.matched_count,
            'modified_count': result.modified_count,
        }

    def delete_one(self, collection, filter):
        result = self.db[collection].delete_one(filter)
        return {
            'deleted_count': result.deleted_count,
        }

    def delete_many(self, collection, filter):
        result = self.db[collection].delete_many(filter)
        return {
            'deleted_count': result.deleted_count,
        }
