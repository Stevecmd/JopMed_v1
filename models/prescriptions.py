#!/usr/bin/python
""" holds class Prescriptions"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Prescriptions(BaseModel, Base):
    """Representation of Prescriptions"""
    if models.storage_t == 'db':
        __tablename__ = 'prescriptions'
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
        medication = Column(String(255), nullable=False)
        dosage = Column(String(255), nullable=False)
        instructions = Column(String(255), nullable=False)
        prescription_date = Column(DateTime, nullable=False)
        expiration_date = Column(DateTime, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    else:
        user_id = ""
        doctor_id = ""
        medication = ""
        dosage = ""
        instructions = ""
        prescription_date = ""
        expiration_date = ""
        created_at = ""
        updated_at = ""

    def __init__(self, *args, **kwargs):
        """initializes prescriptions"""
        super().__init__(*args, **kwargs)
