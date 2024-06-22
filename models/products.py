from sqlalchemy import ForeignKey
from models.farmers import Farmers
from flask import Flask
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import urllib.parse

Base = declarative_base()
app = Flask(__name__)

password = "kayla@2020"
encoded_password = urllib.parse.quote_plus(password)
DATABASE_URL = f"mysql+pymysql://farmlink_user:{encoded_password}@localhost:3306/fm_ln_0"

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

class Product(Base):
	"""Product class"""

	__tablename__ = "products"

	id = Column(Integer, primary_key=True)
	Name = Column(String(100), nullable=False)
	Description = Column(String(200), nullable=False)
	Price = Column(Integer, nullable=False)
	QuantityAvailable = Column(Integer, nullable=False)
	farmers_id = Column(Integer, ForeignKey('farmers.id'), nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
	
	farmer = relationship('Farmers', back_populates='products')

	def __init__(self, id, farmers_id, Name, Description, Price, QuantityAvailable):
		self.id = id
		self.Name = Name
		self.Description = Description
		self.farmers_id = farmers_id
		self.Name = Name
		self.Price = Price
		self.QuantityAvailable = QuantityAvailable

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
			return f"<Product {self.name}>"

Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run()
