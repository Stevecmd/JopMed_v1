#!/usr/bin/python
""" holds class Tags"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Tags(BaseModel, Base):
    """Representation of Tags"""
    if models.storage_t == 'db':
        __tablename__ = 'tags'
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        name = Column(String(255), nullable=False)
        slug = Column(String(255), nullable=False, unique=True)
        description = Column(Text, nullable=True)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

        # Relationships (if needed)
        products = relationship("Product", secondary="products_tags", back_populates="tags")

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
