from sqlalchemy.orm import Session
from .models import User
from . import models, schemas
from .jwt import hasher
from secrets import token_urlsafe


def create_activate_code():
    code = token_urlsafe(12)
    return code


def create_user(db: Session, data: schemas.UserCreate):
    query_data = db.query(models.User).filter(models.User.email == data.email).first()

    if query_data:
        return False
    data.password = hasher.get_password_hash(data.password)
    db_data = models.User(**data.dict(), activation_code=create_activate_code())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_user(username: str, db: Session):
    user = db.query(User).filter(User.email == username).first()
    return user


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username=username, db=db)
    if not user:
        return False
    if not hasher.verify_password(password, user.password):
        return False
    return user


def create_superuser(db: Session, user):
    user.is_superuser = True
    db.commit()
    return user