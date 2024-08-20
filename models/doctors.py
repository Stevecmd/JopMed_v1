#!/usr/bin/python
""" holds class Doctors"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Doctors(BaseModel, Base):
    """Representation of Doctors"""
    __tablename__ = 'doctors'
    
    if models.storage_t == 'db':
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(128), nullable=False)
        specialization = Column(String(128), nullable=False)
        phone_number = Column(String(128), unique=True, nullable=False)
    else:
        id = ""
        name = ""
        specialization = ""

    def __init__(self, *args, **kwargs):
        """initializes comment"""
        super().__init__(*args, **kwargs)