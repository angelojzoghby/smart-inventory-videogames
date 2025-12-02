from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from services.price_model_service import predict as predict_price, load_model

router = APIRouter()

class PredictRequest(BaseModel):
    payload: Dict[str, Any]

@router.post('/predict-price')
def predict(req: PredictRequest):
    try:
        price = predict_price(req.payload)
        return { 'price_predicted': price }
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Prediction error: {e}')
