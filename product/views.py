from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from . import models, schemas
from .helpers import my_exception, my_permission


def get_product(db: Session, product_id: int):
    return db.query(models.Product).get(product_id)


def get_all_product(db: Session):
    print(db.query(models.Product).all())
    return db.query(models.Product).all()


def create_product(db: Session, product: schemas.ProductCreate, user, image):
    if not get_one_cat(db=db, id=product.category_id):
        raise my_exception.not_exist_item()
    data = jsonable_encoder(product)
    db_product = models.Product(**data, image=image, user=user)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def drop_product(db: Session, product_id: int, product_user):
    product_query = get_product(db, product_id)
    if not product_query:
        raise my_exception.not_exist_item()
    if not product_query.user == product_user:
        raise my_exception.unauthorized_exception()

    db.query(models.Product).filter(models.Product.id == product_id).delete()
    db.commit()
    return None


def update_product(db: Session, product_id: int | schemas.ProductResponse, data: schemas.ProductUpdate, product_user):
    product_query = get_product(db, product_id)

    if not product_query:
        raise my_exception.not_exist_item()
    if not product_query.user == product_user:
        raise my_exception.unauthorized_exception()
    for key, value in data:
        setattr(product_query, key, value)
    db.commit()
    return product_query


def get_one_cat(db: Session, cat=None, id=None):
    if cat:
        res = db.query(models.Category).filter(models.Category.title == cat.title).first()
        return res
    if id:
        res = db.query(models.Category).filter(models.Category.id == id).first()
        return res
    return None


def get_all_categories(db: Session):
    all_categories = db.query(models.Category).all()
    return all_categories


def create_category(data, db: Session, user):
    if not user.is_superuser:
        raise my_exception.not_admin()
    if get_one_cat(db=db, cat=data):
        raise my_exception.exist_item()

    jsonable_data = jsonable_encoder(data)
    db_category = models.Category(**jsonable_data)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def drop_category(categories_id, db: Session, user):
    if not user.is_superuser:
        raise my_exception.not_admin()

    get_category = db.query(models.Category).filter(models.Category.id == categories_id)
    if not get_category.first():
        raise my_exception.not_exist_item()
    get_category.delete()
    db.commit()
    return None

