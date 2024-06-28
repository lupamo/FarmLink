#!/usr/bin/python3
from sqlalchemy import ForeignKey
from flask import Flask
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base
import urllib.parse
from models.products import Product
from models.farmers import Farmers

Base = declarative_base()
app = Flask(__name__)


password = "kayla@2020"
encoded_password = urllib.parse.quote_plus(password)
DATABASE_URL = f"mysql+pymysql://farmlink_user:{encoded_password}@localhost:3306/fm_ln_0"

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

class Review(Base):
	"""Class Review"""

	__tablename__ = "reviews"

	id = Column(Integer, primary_keys=True)
	product_id = Column(Integer, ForeignKey('products.id'),nullable=False)
	farmer_id = Column(Integer, ForeignKey('farmers.id'), nullable=False)
	comment = Column(String(500), nullable=False)
	rating = Column(Integer, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Colmn(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	product = relationship('Product', back_populates='reviews')
	farmer = relationship('Farmers', back_populates='reviews')

	def __init__(self, product_id, farmer_id, comment, rating):
		self.product_id = product_id
		self.farmer_id = farmer_id
		self.comment = comment
		self.rating = rating

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
		return f"<Review {self.review_text}>"

Product.reviews = relationship('Review', order_by=Review.id, back_populates='product')
Farmers.reviews = relationship('Review', order_by=Review.id, back_populates='farmer')

Base.metadata.create_all(engine)

if __name__ == "__main__":
	app.run()

	# Create a new review and save it to the database
	review1 = Review(product_id=1, farmer_id=1, review_text="Great product!", rating=5)
	review1.save()

	# Query all review
	session = Session()
	reviews = session.query(Review).all()
	print(reviews)

