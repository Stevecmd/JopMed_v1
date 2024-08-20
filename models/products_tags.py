#!/usr/bin/python
""" holds class Product_Tags"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship


class Product_Tags(BaseModel, Base):
    """Representation of Product_Tags"""
    if models.storage_t == 'db':
        __tablename__ = 'products_tags'
        product_id = Column(Integer, ForeignKey('products.id'), primary_key=True, nullable=False)
        tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True, nullable=False)


    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
