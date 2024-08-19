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
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
