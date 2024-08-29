#!/usr/bin/python
""" holds class Association Tables"""
from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base_model import Base

products_tags = Table('products_tags', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)
