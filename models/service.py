# models/service.py
import models
from models.base_model import BaseModel, Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    DECIMAL,
    ForeignKey,
    Text,
    DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime

class Service(BaseModel, Base):
    """Representation of a Service"""
    if models.storage_t == 'db':
        __tablename__ = 'services'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(255), nullable=False)
        description = Column(Text, nullable=False)
        price = Column(DECIMAL(10, 2), nullable=False)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
        image_url = Column(String(255), nullable=True)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

        # Define relationships
        user = relationship("User", back_populates="services")
        order = relationship("Orders", back_populates="services")
        cart_items = relationship("ShoppingCart", back_populates="service")

    def __init__(self, *args, **kwargs):
        """initializes service"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Convert instance to dictionary format for JSON serialization"""
        service_dict = super().to_dict()
        return service_dict
