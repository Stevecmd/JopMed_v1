#!/usr/bin/python
""" holds class Orders"""
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship


class Orders(BaseModel, Base):
    """Representation of Orders """
    __tablename__ = 'orders'
    if models.storage_t == "db":

       id = Column(Integer, primary_key=True, autoincrement=True)
       user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
       address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
       status = Column(Enum('pending', 'shipped', 'delivered', 'cancelled'), nullable=False)
       payment_method = Column(Enum('credit_card', 'debit_card', 'paypal', 'cash_on_delivery'), nullable=False)
       total_amount = Column(DECIMAL(10, 2), nullable=False)
       created_at = Column(DateTime, nullable=False)
       updated_at = Column(DateTime, nullable=False)

       user = relationship("User", back_populates="orders")
       address = relationship("Address", back_populates="orders")

    else:
        user_id = ""
        address_id = ""
        status = ""
        payment_method = ""
        total_amount = 0
        created_at = ""
        updated_at = ""


    def __init__(self, *args, **kwargs):
        """initializes addresses"""
        super().__init__(*args, **kwargs)
