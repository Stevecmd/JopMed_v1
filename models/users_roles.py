#!/usr/bin/python
""" holds class UserRoles"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class User_Roles(BaseModel, Base):
    """Representation of UserRoles"""
    if models.storage_t == 'db':
        __tablename__ = 'user_roles'
        id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes user roles"""
        super().__init__(*args, **kwargs)