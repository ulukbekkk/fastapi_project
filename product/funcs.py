from fastapi import Depends, HTTPException, APIRouter, status, Request, Form, UploadFile, File
from fastapi.security import HTTPBearer

from sqlalchemy.orm import Session

from db_config.db import engine

from . import models, schemas, views
from account.funcs import get_current_user_from_token

from dependcies.dependss import get_db
from .helpers import my_permission
models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Products"], prefix='/products')
router_cat = APIRouter(tags=['Category'], prefix='/categories')

http_bearer = HTTPBearer()


@router.get('/', response_model=list[schemas.ProductResponse])
async def get_all_product(db: Session = Depends(get_db)):
    return views.get_all_product(db=db)


@router.get('/{product_id}', response_model=schemas.ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):

    product = views.get_product(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail={'message': 'this is product have not'})
    return product


@router.post('/', response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(title: str = Form(),
                   category_id: int = Form(),
                   image: UploadFile = File(...),
                   db: Session = Depends(get_db),
                   user=Depends(get_current_user_from_token)):
    product = schemas.ProductCreate(title=title, category_id=category_id)
    new_product = views.create_product(db=db, product=product, user=user, image=image)
    return new_product


@router.put('/{product_id}', response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductUpdate,
                   db: Session = Depends(get_db), user=Depends(get_current_user_from_token)):

    product_data = views.update_product(db=db, product_id=product_id, data=product, product_user=user)
    if not product_data:
        raise HTTPException(status_code=404, detail={'message': 'No product with this is id '})
    return product_data


@router.delete('/{product_id}', status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db),
                   user=Depends(get_current_user_from_token)):

    views.drop_product(db=db, product_id=product_id, product_user=user)
    return {'msg': 'Deleted'}


@router_cat.post('/', response_model=schemas.CategoryResponse)
def create_category_admin(category: schemas.CategoryCreate, db: Session = Depends(get_db),
                          user=Depends(get_current_user_from_token)):

    post = views.create_category(data=category, db=db, user=user)
    return post


@router_cat.delete('/{categories_id}')
def delete_category_admin(categories_id: int, db: Session = Depends(get_db),
                          user=Depends(get_current_user_from_token)):

    views.drop_category(categories_id=categories_id, db=db, user=user)
    return {'msg': status.HTTP_204_NO_CONTENT}


@router_cat.get('/', response_model=list[schemas.CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    res = views.get_all_categories(db=db)
    return res




