#!/usr/bin/python
""" holds class File_Uploads"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class File_Uploads(BaseModel, Base):
    """Representation of File Uploads"""
    __tablename__ = 'file_uploads'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    file_name = Column(String(128), nullable=False)
    file_path = Column(String(256), nullable=False)
    upload_date = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    # Define relationship with Category if needed
    category = relationship("Category", back_populates="file_uploads")

    def __init__(self, *args, **kwargs):
        """Initialization of file uploads"""
        super().__init__(*args, **kwargs)
