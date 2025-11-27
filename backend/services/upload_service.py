from utils.gridfs import save_image_to_gridfs

async def handle_image_upload(file):
    contents = await file.read()
    image_id = save_image_to_gridfs(contents, file.filename)

    return {
        "image_id": image_id,
        "product_type": "Game",
        "product_name": "Sample Game",
        "price_predicted": 19.99
    }
