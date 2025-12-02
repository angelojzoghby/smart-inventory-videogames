from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes_upload import router as upload_router
from api.routes_inventory import router as inventory_router
from api.routes_images import router as images_router

app = FastAPI()

# CORS settings for local development
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(inventory_router)
app.include_router(images_router)

@app.get("/ping")
def ping():
    return {"status": "ok"}
