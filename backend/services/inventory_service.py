import uuid
import datetime
from database.mongo import products_collection

def add_product_service(data):
    product_id = str(uuid.uuid4())
    price_modified = data.price_modified or data.price_predicted

    product_doc = {
        "product_id": product_id,
        "product_name": data.product_name,
        "product_type": data.product_type,
        "image_id": data.image_id,
        "price_predicted": data.price_predicted,
        "price_modified": price_modified,
        "quantity": data.quantity,
        "date_added": datetime.datetime.utcnow()
    }

    products_collection.insert_one(product_doc)
    return {"status": "success", "product_id": product_id}

def list_products_service():
    return list(products_collection.find({}, {"_id": 0}))

def update_quantity_service(data):
    products_collection.update_one(
        {"product_id": data.product_id},
        {"$set": {"quantity": data.quantity}}
    )
    return {"status": "quantity updated"}

def update_price_service(data):
    products_collection.update_one(
        {"product_id": data.product_id},
        {"$set": {"price_modified": data.price_modified}}
    )
    return {"status": "price updated"}

def get_single_product_service(product_id: str):
    return products_collection.find_one(
        {"product_id": product_id},
        {"_id": 0}
    )
