#!/usr/bin/env python3

from sqlalchemy import ForeignKey
from models.farmers import Farmers, Base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
import urllib.parse

password = "kayla@2020"
encoded_password = urllib.parse.quote_plus(password)
DATABASE_URL = f"mysql+pymysql://farmlink_user:{encoded_password}@localhost:3306/fm_ln_0"

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

class Product(Base):
	"""Product class"""

	__tablename__ = "products"

	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	price = Column(Integer, nullable=False)
	quantity = Column(Integer, nullable=False)
	farmer = Column(Integer, ForeignKey("farmers.id"), nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


	def __init__(self, name, price, quantity, farmer):
			self.name = name
			self.price = price
			self.quantity = quantity
			self.farmer = farmer

	def save(self):
			session = Session()
			session.add(self)
			try:
				session.commit()
			except Exception as e:
				session.rollback()
				raise e
			finally:
				session.close()

	def delete(self):
		session = Session()
		session.delete(self)
		session.commit()
		session.close()

	def __repr__(self):
            return f"<Product {self.name} {self.price} {self.quantity} {self.farmer}>"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# add a new product

product1 = Product(name= "Tomatoes", price=100, quantity=4, farmer=2)
product2 = Product(name= "Vegetables", price=200, quantity=6, farmer=2)
product3 = Product(name= "Watermelon", price=300, quantity=2, farmer=2)

# session.add(product1)
# session.add(product2)
# session.add(product3)
# session.commit()
# session.close()
