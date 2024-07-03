#!/usr/bin/env python3

from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base
import urllib.parse

Base = declarative_base()

password = "kayla@2020"
encoded_password = urllib.parse.quote_plus(password)
DATABASE_URL = f"mysql+pymysql://farmlink_user:{encoded_password}@localhost:3306/fm_ln_0"

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

class Customers(Base):
	"""customers class"""

	__tablename__ = "customers"

	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	contact = Column(Integer, nullable=False)
	address = Column(String(255), nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	def __init__(self, name, contact, address):
		self.name = name
		self.contact = contact
		self.address = address

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
			return f"<Customers {self.name} {self.contact} {self.address}>"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#add a new customer
customer1 = Customers(name="Loice Wamse", contact="0754083545", address="Nairobi")
customer2 = Customers(name="Harri Maina", contact="0702345765", address="Nairobi")
session.add(customer1)
session.add(customer2)
session.commit()
results = session.query(Customers).all()
print(results)
