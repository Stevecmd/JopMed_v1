#!/usr/bin/python
""" holds class Roles"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Roles(BaseModel, Base):
    """Representation of Roles"""
    if models.storage_t == 'db':
        __tablename__ = 'roles'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(255), nullable=False, unique=True)
        description = Column(Text, nullable=True)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False
        )

    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
