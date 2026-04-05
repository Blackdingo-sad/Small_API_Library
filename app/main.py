from fastapi import FastAPI

from app.core.config import settings
from app.db.database import Base, engine
from app.models.book import Book  # noqa: F401
from app.routers.books import router as books_router
from app.routers.health import router as health_router

# Auto-create tables for small local projects.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(health_router)
app.include_router(books_router)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}
