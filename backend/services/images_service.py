from bson import ObjectId
from utils.gridfs import fs

def get_image_service(image_id: str):
    try:
        file = fs.get(ObjectId(image_id))
        return file.read()
    except:
        return None
