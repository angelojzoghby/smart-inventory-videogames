from utils.gridfs import save_image_to_gridfs
from PIL import Image
from io import BytesIO
from fastapi import HTTPException

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

try:
    from services.classification_service import predict_image
except:
    predict_image = None

async def handle_image_upload(file):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")

    contents = await file.read()

    try:
        Image.open(BytesIO(contents))
    except:
        raise HTTPException(400, "Invalid image")

    image_id = save_image_to_gridfs(contents, file.filename)

    title = "Unknown Game"
    genres = ["Action"]

    if callable(predict_image):
        try:
            name, g = predict_image(contents)
            if name:
                title = name
            if g:
                genres = [g] if isinstance(g, str) else g
        except:
            pass

    from database.mongo import products_collection
    existing = products_collection.find_one(
        {"product_name": title},
        {"_id": 0}
    )

    return {
        "image_id": image_id,
        "title": title,
        "genres": genres,
        "exists": existing is not None,
        "product": existing
    }
