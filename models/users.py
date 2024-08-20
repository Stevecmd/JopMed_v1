#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
import bcrypt
from datetime import datetime


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        username = Column(String(64), nullable=False, unique=True)
        email = Column(String(120), nullable=False, unique=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(300), nullable=False)
        last_name = Column(String(300), nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        comments = relationship("Comments", back_populates="user")
        orders = relationship("Orders", back_populates="user")
        reviews = relationship("Reviews", back_populates="user")
        shipping_information = relationship(
            "Shipping_Information",
            back_populates="user"
        )

    else:
        username = ""
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        comments = []
        reviews = []

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with bcrypt encryption"""
        if name == "password":
            value = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
        super().__setattr__(name, value)
