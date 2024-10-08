#!/usr/bin/python
""" holds class Reviews"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship


class Reviews(BaseModel, Base):
    """Representation of Reviews"""
    if models.storage_t == 'db':
        __tablename__ = 'reviews'
        id = Column(
            Integer,
            primary_key=True,
            nullable=False,
            autoincrement=True
        )
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
        rating = Column(Integer, nullable=False)
        comment = Column(Text, nullable=True)
        created_at = Column(
            sqlalchemy.DateTime,
            nullable=False,
            default=sqlalchemy.func.now()
        )
        updated_at = Column(
            sqlalchemy.DateTime,
            nullable=False,
            default=sqlalchemy.func.now(),
            onupdate=sqlalchemy.func.now()
        )

        user = relationship("User", back_populates="reviews")
        product = relationship("Products", back_populates="reviews")

        __table_args__ = (UniqueConstraint('user_id', 'product_id', name='_user_product_uc'),)

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
