from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.database import engine, Base
from routes.hello import router as hello_router
from routes.items import router as items_router
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    Base.metadata.create_all(bind=engine)
    yield
    # SHUTDOWN (cleanup goes here if needed)

app = FastAPI(
    title=settings.title,
    description="Learning every FastAPI routing concept.",
    version=settings.version,
    lifespan=lifespan,
)

app.include_router(hello_router)
app.include_router(items_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)
