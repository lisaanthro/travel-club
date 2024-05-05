from backend.app.crud import user
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.dependencies import get_db

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.get("/get_all")
def get_all_users(db: Session = Depends(get_db)):
    users = user.get_all_users(db)

    return users
