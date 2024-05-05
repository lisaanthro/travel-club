from backend.app.crud import user
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.dependencies import get_db, current_user
from backend.app import schemas, crud, errors, serializers, models

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.post(path="/register")
def register_user(user: schemas.UserCreateRequest = Body(...),
                  db: Session = Depends(get_db)
                  ) -> schemas.Token:
    try:
        db_user = crud.create_user(db, user)
    except errors.EmailAlreadyAssociatedError as e:
        raise HTTPException(status_code=409, detail=str(e))
    db_token = crud.create_token(db, db_user.id)

    return serializers.get_token(db_token)


@user_router.post(path="/login")
def login_user(user: schemas.UserLoginRequest = Body(...),
               db: Session = Depends(get_db)
               ) -> schemas.Token:
    try:
        db_user = crud.read_user_by_login(db, user)
    except errors.AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    db_token = crud.create_token(db, db_user.id)

    return serializers.get_token(db_token)


@user_router.get(path="/profile")
def profile_user(user: models.User = Depends(current_user),
                 db: Session = Depends(get_db)
                 ) -> schemas.User:
    return serializers.get_user(user)


@user_router.get("/get_all")
def get_all_users(db: Session = Depends(get_db)):
    users = user.get_all_users(db)

    return users
