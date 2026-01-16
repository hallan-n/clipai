from consts import MONGO_CONN
from pymongo import MongoClient
from services.logger import logger


def _get_conn(db: str, collection: str):
    client = MongoClient(MONGO_CONN)
    db = client[db]
    collection = db[collection]
    return collection


def add_data(data, db: str, collection: str):
    connection = _get_conn(db, collection)
    logger.info("Adicionando dados ao MongoDB")
    connection.insert_one(data)


def find_last(db: str, collection: str):
    connection = _get_conn(db, collection)
    logger.info("Buscando último dado no MongoDB")
    return connection.find_one(sort=[("_id", -1)])
