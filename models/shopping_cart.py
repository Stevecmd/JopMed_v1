#!/usr/bin/python
""" holds class ShoppingCart"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class ShoppingCart(BaseModel, Base):
    """Representation of ShoppingCart """
    if models.storage_t == 'db':
        __tablename__ = 'shopping_cart'
        id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
        service_id = Column(Integer, ForeignKey('services.id'), nullable=True)
        quantity = Column(Integer, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

        user = relationship("User", back_populates="cart_items")
        product = relationship("Products", back_populates="cart_items")
        service = relationship("Service", back_populates="cart_items")

    def __init__(self, *args, **kwargs):
        """initializes shopping cart item"""
        super().__init__(*args, **kwargs)


    def to_dict(self):
        """Returns a dictionary representation of the ShoppingCart instance"""
        item_dict = super().to_dict()
        item_dict['product'] = self.product.to_dict(include_image=True) if self.product else None
        item_dict['service'] = self.service.to_dict() if self.service else None
        return item_dict
