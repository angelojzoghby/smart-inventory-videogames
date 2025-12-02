from utils.gridfs import save_image_to_gridfs
from PIL import Image
from io import BytesIO
from fastapi import HTTPException

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

try:
    from services.price_model_service import predict as predict_price
except Exception:
    predict_price = None
try:
    from services.classification_service import predict_image
except Exception:
    predict_image = None

async def handle_image_upload(file):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only JPG, PNG, and WEBP images are allowed."
        )

    contents = await file.read()

    try:
        Image.open(BytesIO(contents))
    except:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid image."
        )

    image_id = save_image_to_gridfs(contents, file.filename)

    product_type = "Game"
    product_name = "Unknown Game"
    price_predicted = 19.99

    if callable(predict_image):
        try:
            name, ptype = predict_image(contents)
            if name:
                product_name = name
            if ptype:
                product_type = ptype
        except Exception:
            pass

    if callable(predict_price):
        try:
            price_predicted = predict_price({ 'product_name': product_name, 'product_type': product_type })
        except FileNotFoundError:
            pass
        except Exception:
            pass

    try:
        from database.mongo import products_collection
        existing = products_collection.find_one({
            "product_name": product_name,
            "product_type": product_type
        }, {"_id": 0})
        if existing:
            return {
                "image_id": image_id,
                "product_type": product_type,
                "product_name": product_name,
                "price_predicted": float(price_predicted),
                "exists": True,
                "product": existing
            }
    except Exception:
        pass

    return {
        "image_id": image_id,
        "product_type": product_type,
        "product_name": product_name,
        "price_predicted": float(price_predicted),
        "exists": False
    }
