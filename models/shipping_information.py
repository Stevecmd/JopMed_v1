#!/usr/bin/python
""" holds class Shipping_Information"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Shipping_Information(BaseModel, Base):
    """Representation of Shipping_Information"""
    if models.storage_t == 'db':
        __tablename__ = 'shipping_information'
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
        shipping_method_id = Column(Integer, ForeignKey('shipping_methods.id'), nullable=False)
        tracking_number = Column(String(255), nullable=True)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

        # Relationships (if needed)
        user = relationship("User", back_populates="shipping_information")
        address = relationship("Address", back_populates="shipping_information")
        shipping_method = relationship("ShippingMethod", back_populates="shipping_information")

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
