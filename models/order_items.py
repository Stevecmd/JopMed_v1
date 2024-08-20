#!/usr/bin/python
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
# from models.amenity import Amenity
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Order_Items(BaseModel, Base):
    """Representation of Orders Items"""
    if models.storage_t == 'db':
        __tablename__ = 'order_items'
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
        product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
        quantity = Column(Integer, nullable=False)
        price = Column(Float, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

        # Relationships
        order = relationship("Order", back_populates="order_items")
        product = relationship("Product", back_populates="order_items")

    else:
        id = ""
        order_id = ""
        product_id = ""
        quantity = 0
        price = 0
        created_at = ""
        updated_at = ""


    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
