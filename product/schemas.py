from pydantic import BaseModel, Field
from datetime import datetime, date
from fastapi import Body, File, UploadFile

from account.schemas import UserResponse


class ProductBase(BaseModel):
    title: str = Field(example='something', max_length=100, min_length=2)
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class ProductResponse(ProductBase):
    id: int
    data: date
    user: UserResponse
    category_id = CategoryResponse

    class Config:
        orm_mode = True



# class UpdateProduct(BaseModel):
#     pass
#     # class Config:
#     #     orm_mode = True
#     #     schema_extra = {
#     #         'title': 'something'
#     #     }

