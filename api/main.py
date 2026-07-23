from fastapi import FastAPI
from routes.hello import router as hello_router
from config import settings 

app = FastAPI(
    title=settings.title,
    description="Learning every FastAPI routing concept.",
    version=settings.version,
)

app.include_router(hello_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)
