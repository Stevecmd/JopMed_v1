#!/usr/bin/python
""" holds class Roles"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Text

class Roles(BaseModel, Base):
    """Representation of Roles"""
    if models.storage_t == 'db':
        __tablename__ = 'roles'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(255), nullable=False, unique=True)
        description = Column(Text, nullable=True)
