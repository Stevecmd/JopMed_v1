#!/usr/bin/python
""" holds class Payments"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Payments(BaseModel, Base):
    """Representation of Payments"""
    if models.storage_t == 'db':
        __tablename__ = 'payments'
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
        payment_status = Column(String(50), nullable=False)
        amount = Column(Float, nullable=False)
        transaction_id = Column(String(255), nullable=False)
        payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    else:
        order_id = ""
        payment_status = ""
        amount = 0
        transaction_id = ""
        payment_date = ""
        created_at = ""
        updated_at = ""

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
