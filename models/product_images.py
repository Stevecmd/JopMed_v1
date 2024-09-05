#!/usr/bin/python
""" holds class Product_Images"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Product_Images(BaseModel, Base):
    """Representation of Product_Images"""
    if models.storage_t == 'db':
        __tablename__ = 'product_images'
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
        image_url = Column(String(255), nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

        product = relationship("Products", back_populates="product_images")

    else:
        product_id = ""
        image_url = ""
        created_at = ""
        updated_at = ""

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
