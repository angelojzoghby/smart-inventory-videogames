from fastapi import APIRouter, UploadFile, File, HTTPException
from services.classification_service import predict_image

router = APIRouter()

@router.post("/classify-image")
async def classify_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(400, "Invalid image format")

    contents = await file.read()

    title, genres = predict_image(contents)

    return {
        "title": title,
        "genres": genres
    }
