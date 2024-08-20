#!/usr/bin/python
""" holds class Product_Tags"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, Table, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship


class Product_Tags(BaseModel, Base):
    """Representation of Product_Tags"""
    if models.storage_t == 'db':
        __tablename__ = 'products_tags'
        id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
        product_id = Column(Integer, ForeignKey('products.id'), primary_key=True, nullable=False)
        tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
