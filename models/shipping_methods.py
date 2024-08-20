#!/usr/bin/python
""" holds class Shipping_Methods"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Shipping_Methods(BaseModel, Base):
    """Representation of Shipping_Methods"""
    if models.storage_t == 'db':
        __tablename__ = 'shipping_methods'
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        name = Column(String(255), nullable=False)
        description = Column(Text, nullable=True)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

        # Relationships (if needed)
        shipping_information = relationship("Shipping_Information", back_populates="shipping_method")

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
