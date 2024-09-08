from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey

class PaymentMethod(BaseModel, Base):
    __tablename__ = 'payment_methods'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    last_four = Column(String(4), nullable=False)