from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from db_config.db import Base


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    activation_code = Column(String)

    product = relationship("Product", back_populates="user")

    def __str__(self):
        return f'{self.email}-{self.is_superuser}, {self.activation_code}'

    def __repr__(self):
        return self.email