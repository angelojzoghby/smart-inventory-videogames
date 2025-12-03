from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.price_model_service import predict as predict_price

router = APIRouter()

class PredictRequest(BaseModel):
    title: str
    genres: List[str]
    dlc: int
    gamepass: int
    franchise: int
    discount: int

@router.post("/predict-price")
def predict_price_endpoint(req: PredictRequest):
    try:
        return {"price_predicted": predict_price(req.dict())}
    except Exception as e:
        raise HTTPException(500, str(e))
