#!/usr/bin/env python3
import os
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime
import urllib.parse
from .base import Base


password = "kayla@2020"
encoded_password = urllib.parse.quote_plus(password)
DATABASE_URL = f"mysql+pymysql://farmlink_user:{encoded_password}@localhost:3306/fm_ln_0"

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

class Product(Base):
    """Product class"""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    Description = Column(String(300), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    image = Column(String(300)) 
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    farmer = relationship("Farmers", back_populates="products")

    def __init__(self, name, Description, price, quantity, farmer_id, image=None):
        self.name = name
        self.Description = Description
        self.price = price
        self.quantity = quantity
        self.farmer_id = farmer_id
        self.image = image

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
        return f"<Product {self.name} {self.Description} {self.price} {self.quantity} {self.farmer_id}>"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#adding a product
#product1 = Product(name="carrots", Description="freshly picked carrots", price=100, quantity=50, farmer_id=1)
#product2 = Product(name="cabbage", Description="freshly picked cabbage", price=50, quantity=23, farmer_id=2)
#session.add(product1)
#session.add(product2)
#session.commit()
#results = session.query(Product).all()
#print(results)