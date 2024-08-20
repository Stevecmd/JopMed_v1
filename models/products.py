#!/usr/bin/python
""" holds class Products"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table, Text, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime


class Products(BaseModel, Base):
    """Representation of Products """
    if models.storage_t == 'db':
        __tablename__ = 'products'
        name = Column(String(255), nullable=False)
        description = Column(Text)
        price = Column(DECIMAL(10, 2), nullable=False)
        stock = Column(Integer, nullable=False)
        category = Column(String(255))
        slug = Column(String(255))
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
        comments = relationship("Comments", back_populates="product")
