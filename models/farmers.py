#!/usr/bin/env python3

import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
import urllib.parse
from .base import Base
from models.products import Product


load_dotenv()

"""configuring the database connection"""
password = "kayla@2020"
encoded_password = urllib.parse.quote_plus(password)
DATABASE_URL = f"mysql+pymysql://farmlink_user:{encoded_password}@localhost:3306/fm_ln_0"

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))


class Farmers(Base):
    """farmers class creation"""

    __tablename__ = 'farmers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact = Column(Integer, unique=True, nullable=False)
    address = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to products
    products = relationship("Product", back_populates="farmer")

    def __init__(self, name, contact, address):
        self.name = name
        self.contact = contact
        self.address = address
    
    def save(self):
        """Saving farmers info to the database"""
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
        """Deleting farmers info from the database"""
        session = Session()
        session.delete(self)
        session.commit()
        session.close()

    def __repr__(self):
        return f"<Farmers (name={self.name}, contact={self.contact}, address={self.address})>"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
