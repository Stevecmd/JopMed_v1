#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
import models
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
from models.wishlist import Wishlist
from hashlib import md5

classes = {"Addresses": Addresses, "BaseModel": BaseModel,
           "Categories": Categories, "Comments": Comments,
           "Doctors": Doctors, "File_Uploads": File_Uploads,
           "Inventory": Inventory, "Order_Items": Order_Items,
           "Orders": Orders, "Payment_Information": Payment_Information,
           "Payments": Payments, "Product_Categories": Product_Categories,
           "Product_Tags": Product_Tags, "Product": Product_Tags,
           "Products": Products, "Products": Products,
           "Reviews": Reviews,
           "Roles": Roles, "Shipping_Information": Shipping_Information,
           "Shipping_Methods": Shipping_Methods, "Tags": Tags,
           "User_Roles": User_Roles, "User": User,
           "Wishlist": Wishlist}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            if key == "password":
                json_objects[key].decode()
            json_objects[key] = self.__objects[key].to_dict(save_fs=1)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
