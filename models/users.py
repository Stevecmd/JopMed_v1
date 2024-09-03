#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True, autoincrement=True)
        username = Column(String(64), nullable=False, unique=True)
        email = Column(String(120), nullable=False, unique=True)
        password_hash = Column(String(512), nullable=False)
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
        wishlist_items = relationship("Wishlist", back_populates="user")
        services = relationship("Service", back_populates="user")


    else:
        username = ""
        email = ""
        password_hash = ""
        first_name = ""
        last_name = ""
        comments = []
        reviews = []

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def set_password(self, password):
        """Hashes the password and stores it in the password_hash field

        Args:
            password (str): The plain text password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the hashed password against the stored hash

        Args:
            password (str): The plain text password

        Returns:
            bool: True if the password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
