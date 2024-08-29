#!/usr/bin/python
""" holds class Product_Categories"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Product_Categories(BaseModel, Base):
    """Representation of Product_Categories"""
    if models.storage_t == 'db':
        __tablename__ = 'product_categories'
        id = Column(Integer, primary_key=True, autoincrement=True)
        product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
        category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    else:
        id = None
        product_id = ""
        category_id = ""
        created_at = None
        updated_at = None

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
