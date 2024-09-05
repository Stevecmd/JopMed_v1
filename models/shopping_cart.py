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
        user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
        product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
        quantity = Column(Integer, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

        user = relationship("User", back_populates="cart_items")
        product = relationship("Products", back_populates="cart_items")

    def __init__(self, *args, **kwargs):
        """initializes shopping cart item"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Returns a dictionary representation of the ShoppingCart instance"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product': self.product.to_dict() if self.product else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
