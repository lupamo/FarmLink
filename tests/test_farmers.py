from flask_testing import TestCase
import models
from models.farmers import app, db, Farmers


class TestFarmersModel(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # Use an in-memory SQLite database for testing
        return app

    def setUp(self):
        db.create_all()  # Creates the database tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()  # Drops the database tables after each test

    def test_farmers_model(self):
        farmer = Farmers(name='John Doe', contact='0778767908', address='Nakuru')
        db.session.add(farmer)
        db.session.commit()
        
        retrieved_farmer = Farmers.query.filter_by(name='John Doe').first()
        self.assertIsNotNone(retrieved_farmer)
        self.assertEqual(retrieved_farmer.name, 'John Doe')
