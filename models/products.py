from sqlalchemy import ForeignKey
from models.farmers import Farmers
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
	"""Product class"""

	__tablename__ = "products"

	id = Column(Integer, primary_key=True)
	Name = Column(String(100), nullable=False)
	Description = Column(String(200), nullable=False)
	price = Column(Integer, nullable=False)
	QuantityAvailable = Column(Integer, nullable=False)
	farmers_id = Column(Integer, ForeignKey('farmers.id'), nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 

	