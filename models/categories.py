#!/usr/bin/python
""" holds class Categories"""
from datetime import datetime, timezone
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship

class Categories(BaseModel, Base):
    """Representation of Categories"""
    if models.storage_t == 'db':
        __tablename__ = 'categories'
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        name = Column(String(255), nullable=False)
        description = Column(Text, nullable=True)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

        products = relationship("Products", secondary="product_categories", back_populates="categories")
        file_uploads = relationship("File_Uploads", back_populates="category")
    else:
        name = ""
        description = ""

    def __init__(self, *args, **kwargs):
        """initializes Categories"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Returns a dictionary representation of the Categories instance"""
        dict_rep = super().to_dict()
        dict_rep.update({
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        })
        return dict_rep