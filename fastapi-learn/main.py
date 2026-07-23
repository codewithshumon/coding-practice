from fastapi import FastAPI
from routes.hello import router as hello_router

app = FastAPI(
    title="FastAPI Learning Lab",
    description="Learning every FastAPI routing concept.",
    version="1.0.0",
)

app.include_router(hello_router)
