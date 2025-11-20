from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import main_router
from app.core.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.include_router(main_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def read_root():
    return {"message": "Backend is running"}


@app.get("/")
def health_check():
    return {"message": "Welcome to Incident Tracker API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
