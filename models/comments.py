#!/usr/bin/python
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Comments(BaseModel, Base):
    """Representation of Comments """
    if models.storage_t == 'db':
        __tablename__ = 'comments'
        id = Column(Integer, primary_key=True, autoincrement=True)
        product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        content = Column(Text, nullable=False)
        created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
        updated_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, onupdate=datetime.now(timezone.utc))

        # Define relationships
        product = relationship("Products", back_populates="comments")
        user = relationship("User", back_populates="comments")
    else:
        product_id = ""
        user_id = ""
        content = ""

    def __init__(self, *args, **kwargs):
        """initializes comment"""
        super().__init__(*args, **kwargs)

