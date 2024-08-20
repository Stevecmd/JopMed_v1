#!/usr/bin/python3
""" holds class Addresses"""
from datetime import datetime, timezone
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Addresses(BaseModel, Base):
    """Representation of Addresses """
    __tablename__ = 'addresses'
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True, nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        city = Column(String(255), nullable=False)
        country = Column(String(255), nullable=False)
        zip_code = Column(String(255), nullable=False)
        street_address = Column(String(255), nullable=False)
        phone_number = Column(String(255))
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        orders = relationship("Orders", back_populates="address")
        shipping_information = relationship(
            "Shipping_Information",
            back_populates="address"
        )
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
