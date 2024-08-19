#!/usr/bin/python
""" holds class Categories"""
from datetime import datetime, timezone
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table, Text, DateTime
from sqlalchemy.orm import relationship


class Categories(BaseModel, Base):
    """Representation of Categories"""
    if models.storage_t == 'db':
        __tablename__ = 'categories'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(255), nullable=False)
        slug = Column(String(255), unique=True, nullable=False)
        description = Column(Text, nullable=True)
        created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
        updated_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, onupdate=datetime.now(timezone.utc))
    else:
        name = ""
        slug = ""
        description = ""

    def __init__(self, *args, **kwargs):
        """initializes category"""
        super().__init__(*args, **kwargs)

