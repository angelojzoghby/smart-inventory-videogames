from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["vg_db"]
products_collection = db["products"]