import datetime

from db_config.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import sqlalchemy as sa


class Category(Base):

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(100), unique=True)

    product = relationship('Product', back_populates='category')

    def __repr__(self):
        return f"Categories <id-{self.id}, title-{self.title}>"


class Product(Base):

    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(100), nullable=False)
    image = Column(String, nullable=False)
    data = Column(DateTime(timezone=True), server_default=func.now())

    user_email = Column(String, ForeignKey('user.email'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    category = relationship('Category', back_populates='product')
    user = relationship("User", back_populates="product")

    def __repr__(self):
        return f'Product <id -{self.id}, title-{self.title}, image-{self.image}, ' \
               f'date-{self.data}, user-{self.user}, category-{self.category},' \
               f'{self.user_email}, {self.category_id}>'

