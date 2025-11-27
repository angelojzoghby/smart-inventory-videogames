from fastapi import APIRouter, UploadFile, File
from services.upload_service import handle_image_upload

router = APIRouter()

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    return await handle_image_upload(file)
