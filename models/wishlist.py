#!/usr/bin/python3
""" holds class Wishlist"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Wishlist(BaseModel, Base):
    """Representation of a wishlist item"""
    __tablename__ = 'wishlist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Define relationship to User model
    user = relationship("User", back_populates="wishlist_items")

    def __init__(self, *args, **kwargs):
        """initializes wishlist item"""
        super().__init__(*args, **kwargs)
