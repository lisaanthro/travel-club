from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from app import db, routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    db.BaseSqlModel.metadata.create_all(bind=db.engine)
    yield


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(routers.user.user_router)

    @_app.get("/info")
    async def download_file():
        file_path = "app/info.pdf"  # Укажи полный путь к файлу на сервере
        file_path = Path(file_path)

        if not file_path.is_file():
            return {"error": "Файл не найден"}

        return FileResponse(path=file_path, filename=file_path.name)

    return _app