#!/usr/bin/python
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
# from models.amenity import Amenity
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


class Order_Items(BaseModel, Base):
    """Representation of Place """
    if models.storage_t == 'db':
        __tablename__ = 'places'
 
