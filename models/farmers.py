#!/usr/bin/python
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
import urllib.parse

load_dotenv()


"""configuring the database connection"""
password = "kayla@2020"
encoded_password = urllib.parse.quote_plus(password)
DATABASE_URL = f"mysql+pymysql://farmlink_user:{encoded_password}@localhost:3306/fm_ln_0"

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

"""Defining a base class"""
Base = declarative_base()


class Farmers(Base):
	"""farmers class creation"""

	__tablename__ = 'farmers'

	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	contact = Column(Integer, unique=True, nullable=False)
	location = Column(String(200), nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	def __init__(self, name, contact, location):
		"""
		farmers class attributes detail
		"""
		self.name = name
		self.contact = contact
		self.location = location
	
	def save(self):
		""""
		Saving farmers info to the database
		"""

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
		""""
		Deleting farmers info to the database
		"""
		session = Session()
		session.delete(self)
		session.commit()
		session.close()
	
	def __repr__(self):
		return f"<farmer {self.name}>"
	
Base.metadata.create_all(engine)

if __name__ == "__main__":
	app.run()
	