from fastapi import Depends, HTTPException, APIRouter, status, Request
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import schemas, views
from dependcies.dependss import get_db
from .jwt import *
from product.helpers import my_exception

from jose import JWTError
import pytz

utc = pytz.UTC

router = APIRouter(prefix='/account', tags=['Users'])

security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")

sessions = {}


@router.post('/register', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    query_data = views.create_user(db=db, data=data)
    if not query_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'msg': 'Account with this is email already exist!'})
    return query_data


@router.post("/login", response_model=schemas.Token)
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = views.authenticate_user(username=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    tokens = {"access_token": create_access_token(data={'sub': user.email}, expires_delta=access_token_expires),
              "refresh_token": create_refresh_token(data={'sub': user.email}, expires_delta=refresh_token_expires),
              'token_type': 'bearer'}

    return tokens


def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        exps: int = payload.get("exp")

        if username is None:
            raise credentials_exception
        if exps is None:
            raise credentials_exception
        if sessions.get(username) == token:  # fake_black_list_db
            raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="UNAUTHORIZED",
                                )
    except JWTError:
        raise credentials_exception

    user = views.get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


@router.post("/logout",)
def user_logout(current_user: schemas.UserResponse = Depends(get_current_user_from_token),
                 token: str = Depends(oauth2_scheme)):

    sessions[current_user.email] = token   # fake_black_list_db
    return {'msg': 'Success LogOut'}


@router.post('/register_superuser', response_model=schemas.SuperUserResponse)
def create_admin_user(secret_code: str, db: Session = Depends(get_db), user=Depends(get_current_user_from_token)):
    my_secret_code = 'Hello world'
    if secret_code != my_secret_code:
        raise my_exception.wrong_code()
    super_user = views.create_superuser(db=db, user=user)
    return super_user
