from fastapi import FastAPI
from api.routes_upload import router as upload_router
from api.routes_inventory import router as inventory_router
from api.routes_images import router as images_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(inventory_router)
app.include_router(images_router)

@app.get("/ping")
def ping():
    return {"status": "ok"}
