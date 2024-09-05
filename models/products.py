#!/usr/bin/python
""" holds class Products"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    Table,
    Text,
    DateTime,
    DECIMAL
)
from sqlalchemy.orm import relationship
from datetime import datetime
from models.shopping_cart import ShoppingCart


class Products(BaseModel, Base):
    """Representation of Products """
    if models.storage_t == 'db':
        __tablename__ = 'products'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(255), nullable=False)
        description = Column(Text)
        price = Column(DECIMAL(10, 2), nullable=False)
        stock = Column(Integer, nullable=False)
        category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False
        )
        comments = relationship("Comments", back_populates="product")
        inventory_items = relationship("Inventory", back_populates="product")
        order_items = relationship("Order_Items", back_populates="product")
        reviews = relationship("Reviews", back_populates="product")
        tags = relationship(
            "Tags",
            secondary="products_tags",
            back_populates="products"
        )
        categories = relationship(
            "Categories",
            secondary="product_categories",
            back_populates="products"
        )
        cart_items = relationship("ShoppingCart", back_populates="product")
        product_images = relationship("Product_Images", back_populates="product")

    def to_dict(self, include_image=False):
        product_dict = super().to_dict()
        if include_image:
            main_image = self.product_images[0] if self.product_images else None
            product_dict['image_url'] = main_image.image_url if main_image else None
        return product_dict

    def __init__(self, *args, **kwargs):
        """initializes products"""
        super().__init__(*args, **kwargs)
