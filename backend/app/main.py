from fastapi import FastAPI
import uvicorn

from backend.app.db import BaseSqlModel
from backend.app.db import engine
from backend.app.routers import user

app = FastAPI()
app.include_router(user.user_router)


def create_tables():
    BaseSqlModel.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print(user.user_router.prefix)
    uvicorn.run("main:app")
