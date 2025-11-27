from fastapi import APIRouter
from pydantic import BaseModel
from services.inventory_service import (
    add_product_service,
    list_products_service,
    update_price_service,
    update_quantity_service,
    get_single_product_service
)

router = APIRouter()

class ProductCreate(BaseModel):
    product_name: str
    product_type: str
    price_predicted: float
    price_modified: float | None = None
    quantity: int
    image_id: str

class QuantityUpdate(BaseModel):
    product_id: str
    quantity: int

class PriceUpdate(BaseModel):
    product_id: str
    price_modified: float

@router.post("/inventory/add")
def add_product(data: ProductCreate):
    return add_product_service(data)

@router.get("/inventory/list")
def list_products():
    return list_products_service()

@router.post("/inventory/update-quantity")
def update_quantity(data: QuantityUpdate):
    return update_quantity_service(data)

@router.post("/inventory/update-price")
def update_price(data: PriceUpdate):
    return update_price_service(data)

@router.get("/inventory/{product_id}")
def get_product(product_id: str):
    return get_single_product_service(product_id)
