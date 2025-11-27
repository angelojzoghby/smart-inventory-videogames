from utils.gridfs import save_image_to_gridfs
from PIL import Image
from io import BytesIO
from fastapi import HTTPException

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

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

    return {
        "image_id": image_id,
        "product_type": "Game",
        "product_name": "Sample Game",
        "price_predicted": 19.99
    }
