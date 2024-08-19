#!/usr/bin/python
""" holds class User_Roles"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class User_Roles(BaseModel, Base):
    """Representation of User_Roles"""
    if models.storage_t == 'db':
        __tablename__ = 'users_roles'
        user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
        role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True, nullable=False)

        # Relationships (if needed)
        user = relationship("User", back_populates="roles")
        role = relationship("Role", back_populates="users")
