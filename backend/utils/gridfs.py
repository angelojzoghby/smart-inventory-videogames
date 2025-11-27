from pymongo import MongoClient
from gridfs import GridFS
from database.mongo import db

fs = GridFS(db)

def save_image_to_gridfs(image_bytes, filename):
    file_id = fs.put(image_bytes, filename=filename)
    return str(file_id)

def get_image_from_gridfs(file_id):
    file = fs.get(file_id)
    return file.read()
