#!/usr/bin/python3
""" holds class Addresses"""
import datetime
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Addresses(BaseModel, Base):
    """Representation of Addresses """
    if models.storage_t == "db":
        __tablename__ = 'states'
        id = Column(String(60), primary_key=True, nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        city = Column(String(255), nullable=False)
        country = Column(String(255), nullable=False)
        zip_code = Column(String(255), nullable=False)
        street_address = Column(String(255), nullable=False)
        phone_number = Column(String(255))
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    # if models.storage_t != "db":
        # @property
        # def cities(self):
        #     """getter for list of city instances related to the state"""
        #     city_list = []
        #     all_cities = models.storage.all(City)
        #     for city in all_cities.values():
        #         if city.state_id == self.id:
        #             city_list.append(city)
        #     return city_list
