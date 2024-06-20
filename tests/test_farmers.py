import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.farmers import Base, Farmers

class TestFarmers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a temporary database for testing"""
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
    
    @classmethod
    def tearDownClass(cls):
        """Tear down the database"""
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        """Create a new session for each test"""
        self.session = TestFarmers.Session()

    def tearDown(self):
        """Rollback any changes made during the test and close the session"""
        self.session.rollback()
        self.session.close()

    def test_save_farmer(self):
        """Test saving a farmer to the database"""
        farmer = Farmers(name='John Doe', contact='123456789', location='123 Main St')
        farmer.save()
        
        saved_farmer = self.session.query(Farmers).filter_by(name='John Doe').first()
        self.assertIsNotNone(saved_farmer)
        self.assertEqual(saved_farmer.name, 'John Doe')
        self.assertEqual(saved_farmer.contact, '123456789')
        self.assertEqual(saved_farmer.location, '123 Main St')

    def test_delete_farmer(self):
        """Test deleting a farmer from the database"""
        farmer = Farmers(name='John Doe', contact='123456789', location='123 Main St')
        farmer.save()
        
        farmer.delete()
        
        deleted_farmer = self.session.query(Farmers).filter_by(name='Jane Doe').first()
        self.assertIsNone(deleted_farmer)

if __name__ == '__main__':
    unittest.main()
