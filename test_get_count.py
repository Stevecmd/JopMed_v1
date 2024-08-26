#!/usr/bin/python3
""" Test .get() and .count() methods
"""

import unittest
from models import storage
from models.users import User
from models.orders import Orders

class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def setUp(self):
        """Set up for the tests"""
        self.user = User(username="testuser", email="testuser@example.com", password="password")
        self.user.save()
        self.order = Orders(user_id=self.user.id, status="pending", payment_method="credit_card", total_amount=100.0)
        self.order.save()

    def tearDown(self):
        """Tear down after the tests"""
        storage.delete(self.order)
        storage.delete(self.user)
        storage.save()

    def test_get_user(self):
        """Test the get method for User"""
        user = storage.get(User, self.user.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_get_order(self):
        """Test the get method for Orders"""
        order = storage.get(Orders, self.order.id)
        self.assertIsNotNone(order)
        self.assertEqual(order.status, "pending")

    def test_count_all(self):
        """Test the count method for all classes"""
        count = storage.count()
        self.assertGreaterEqual(count, 2)  # At least 2 objects (User and Orders)

    def test_count_user(self):
        """Test the count method for User"""
        count = storage.count(User)
        self.assertGreaterEqual(count, 1)  # At least 1 User object

    def test_count_orders(self):
        """Test the count method for Orders"""
        count = storage.count(Orders)
        self.assertGreaterEqual(count, 1)  # At least 1 Orders object

if __name__ == "__main__":
    unittest.main()