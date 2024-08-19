#!/usr/bin/python
""" holds class Product_Categories"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


class Product_Categories(BaseModel, Base):
    """Representation of Product_Categories"""
    if models.storage_t == 'db':
        __tablename__ = 'product_categories'
        product_id = Column(Integer, ForeignKey('products.id'), primary_key=True, nullable=False)
        category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True, nullable=False)
