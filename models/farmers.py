#!/usr/bin/python
import os
from flask import Flask
from datetime import datetime
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

"""configuring the database connection"""

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
"""to supress a warning"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""initializing the SQLAlchemy object"""
db = SQLAlchemy(app)

class Farmers(db.Model):
	"""farmers class creation"""

	__tablename__ = 'farmers'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	contact = db.Column(db.String(20), unique=True, nullable=False)
	address = db.Column(db.String(200), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	def __init__(self, name, contact, address):
		"""
		farmers class attributes detail
		"""
		self.name = name
		self.contact = contact
		self.address = address
	
	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		return f"<farmer {self.name}>"

	