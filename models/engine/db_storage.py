#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.addresses import Addresses
from models.categories import Categories
from models.comments import Comments
from models.doctors import Doctors
from models.file_uploads import File_Uploads
from models.inventory import Inventory
from models.order_items import Order_Items
from models.orders import Orders
from models.payment_information import Payment_Information
from models.payments import Payments
from models.prescriptions import Prescriptions
from models.product_categories import Product_Categories
from models.products_tags import Product_Tags
from models.products import Products
from models.product_images import Product_Images
from models.reviews import Reviews
from models.roles import Roles
from models.service import Service
from models.shipping_information import Shipping_Information
from models.shipping_methods import Shipping_Methods
from models.tags import Tags
from models.wishlist import Wishlist
from models.users import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


classes = {"Addresses": Addresses, "BaseModel": BaseModel,
           "Categories": Categories, "Comments": Comments,
           "Doctors": Doctors, "File_Uploads": File_Uploads,
           "Inventory": Inventory, "Order_Items": Order_Items,
           "Orders": Orders, "Payment_Information": Payment_Information,
           "Payments": Payments, "Prescriptions": Prescriptions,
           "Product_Categories": Product_Categories,
           "Product_Tags": Product_Tags, "Products": Products,
           "Product_Images": Product_Images,
           "Reviews": Reviews, "Roles": Roles, "Service": Service,
           "Shipping_Information": Shipping_Information,
           "Shipping_Methods": Shipping_Methods, "Tags": Tags,
           "User": User, "Wishlist": Wishlist}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        JOPMED_MYSQL_USER = getenv('JOPMED_MYSQL_USER')
        JOPMED_MYSQL_PWD = getenv('JOPMED_MYSQL_PWD')
        JOPMED_MYSQL_HOST = getenv('JOPMED_MYSQL_HOST')
        JOPMED_MYSQL_DB = getenv('JOPMED_MYSQL_DB')
        JOPMED_ENV = getenv('JOPMED_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(JOPMED_MYSQL_USER,
                                             JOPMED_MYSQL_PWD,
                                             JOPMED_MYSQL_HOST,
                                             JOPMED_MYSQL_DB))
        if JOPMED_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if clss == "BaseModel":
                continue
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + str(obj.id)
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    @property
    def session(self):
        """Returns the current database session"""
        return self.__session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        if isinstance(id, tuple):
            # Handle composite keys
            query = self.__session.query(cls)
            primary_keys = cls.__table__.primary_key.columns.keys()
            for key, value in zip(primary_keys, id):
                query = query.filter(getattr(cls, key) == value)
            return query.first()
        else:
            try:
                id = int(id)
            except ValueError:
                return None

            all_cls = models.storage.all(cls)
            for value in all_cls.values():
                if value.id == id:
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

    def get_by_email(self, cls, email):
        """Retrieve an object by email"""
        return self.__session.query(cls).filter_by(email=email).first()

    def filter(self, cls, **kwargs):
        """
        Filter objects by given criteria.
        """
        if cls not in classes.values():
            return []

        query = self.__session.query(cls)
        for key, value in kwargs.items():
            query = query.filter(getattr(cls, key) == value)

        return query.all()
