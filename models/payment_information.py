#!/usr/bin/python
""" holds class Payment_Information"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Payment_Information(BaseModel, Base):
    """Representation of Payment info """
    __tablename__ = 'payment_information'
    if models.storage_t == "db":
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        card_number = Column(String(16), nullable=False)
        card_expiry_date = Column(Date, nullable=False)
        card_cvv = Column(String(3), nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    else:
        user_id = ""
        card_number = ""
        card_expiry_date = ""
        card_cvv = ""
        created_at = ""
        updated_at = ""

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
