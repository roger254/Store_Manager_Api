import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from app import create_app, db


class ProductTestCase(unittest.TestCase):
    """Represents Products TestCase"""

    def setUp(self):
        """Initialize test client"""
        self.app = create_app(config_name='testing')
        self.app.testing = True
        self.client = self.app.test_client
        self.product = {
            'product_name': 'Product 1',
            'product_price': 11.0,
            'product_quantity': 2
        }

        # connect app with content
        with self.app.app_context():
            # create tables
            db.create_all()

    def test_product_creation(self):
        """Test API can create a Product --> [POST] req"""

        response = self.client().post('/products/', data=self.product)
        # test correct response
        self.assertEqual(response.status_code, 201)
        # test data in response
        self.assertIn('Product 1', str(response.data))

    def test_api_can_get_all_products(self):
        """TEst the GET request"""
        response = self.client().post('/products/', data=self.product)
        # test response status_code
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/products/')
        # test return status_code\
        self.assertEqual(response.status_code, 200)
        # test data
        self.assertIn('Product 1', str(response.data))


if __name__ == "__main__":
    unittest.main()
