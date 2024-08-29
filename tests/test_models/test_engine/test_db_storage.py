#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.base_model import BaseModel, Base
from models.addresses import Addresses
from models.base_model import BaseModel
from models.categories import Categories
from models.comments import Comments
from models.doctors import Doctors
from models.file_uploads import File_Uploads
from models.inventory import Inventory
from models.order_items import Order_Items
from models.orders import Orders
from models.payment_information import Payment_Information
from models.payments import Payments
from models.product_categories import Product_Categories
from models.products_tags import Product_Tags
from models.products import Products
from models.reviews import Reviews
from models.roles import Roles
from models.shipping_information import Shipping_Information
from models.shipping_methods import Shipping_Methods
from models.tags import Tags
from models.users_roles import User_Roles
from models.users import User
import json
import os
import pep8
import unittest
from models import storage
DBStorage = db_storage.DBStorage

classes = {"Addresses": Addresses, "BaseModel": BaseModel,
           "Categories": Categories, "Comments": Comments,
           "Doctors": Doctors, "File_Uploads": File_Uploads,
           "Inventory": Inventory, "Order_Items": Order_Items,
           "Orders": Orders, "Payment_Information": Payment_Information,
           "Payments": Payments, "Product_categories": Product_Categories,
           "Product_Tags": Product_Tags, "Product": Product_Tags,
           "Products": Products, "Products": Products,
           "Reviews": Reviews,
           "Roles": Roles, "Shipping_Information": Shipping_Information,
           "Shipping_Methods": Shipping_Methods, "Tags": Tags,
           "User_Roles": User_Roles, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_get_db(self):
        """ Tests method for obtaining an instance db storage"""
        # dic = {"name": "Cundinamarca"}
        # instance = State(**dic)
        # storage.new(instance)
        # storage.save()
        # get_instance = storage.get(State, instance.id)
        # self.assertEqual(get_instance, instance)

    def test_count(self):
        """ Tests count method db storage """
        # dic = {"name": "Vecindad"}
        # state = State(**dic)
        # storage.new(state)
        # dic = {"name": "Mexico", "state_id": state.id}
        # city = City(**dic)
        # storage.new(city)
        # storage.save()
        # c = storage.count()
        # self.assertEqual(len(storage.all()), c)
