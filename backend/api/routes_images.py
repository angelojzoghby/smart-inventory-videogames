from fastapi import APIRouter
from fastapi.responses import Response
from services.images_service import get_image_service

router = APIRouter()

@router.get("/image/{image_id}")
def get_image(image_id: str):
    image_bytes = get_image_service(image_id)
    if image_bytes is None:
        return {"error": "Image not found"}
    return Response(content=image_bytes, media_type="image/jpeg")
