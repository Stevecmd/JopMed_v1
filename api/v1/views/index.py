#!/usr/bin/python3
# """ Index """

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
from models.users import User
from models import storage
from .. import app

from flask import Flask, Blueprint, jsonify, request, abort, render_template
from api.v1.views import app_views


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns the status of the API """
    return jsonify({"status": "OK"})


@app_views.route('/', methods=['GET'], strict_slashes=False)
def index():
    return render_template('index.html')


@app.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = {Addresses, BaseModel,
               Categories,  Comments,
               Doctors,  File_Uploads,
               Inventory, Order_Items,
               Orders, Payment_Information,
               Payments, Product_Categories,
               Product_Tags, Product_Tags,
               Products, Products,
               Reviews, Roles, Shipping_Information,
               Shipping_Methods, Tags,
               User}
    names = ["Addresses", "BaseModel", "Categories", "Comments",
             "Doctors", "File_Uploads", "Inventory", "Order_Items",
             "Orders", "Payment_Information", "Payments",
             "Product_categories", "Product_Tags", "Product", "Products",
             "Products", "Reviews", "Roles", "Shipping_Information",
             "Shipping_Methods", "Tags", "User_Roles", "User"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)


@app.route('/product_search/', methods=['POST'], strict_slashes=False)
def search_products():
    """Returns a list of products based on the search criteria"""
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if not data or not len(data):
        products = storage.all(product).values()
        list_products = [product.to_dict() for product in products]
        return jsonify(list_products)

    list_products = []

    products = []
    for product in list_products:
        product_dict = product.to_dict()
        user = storage.get(User, product.user_id)
        product_dict['user'] = user.to_dict()
        products.append(product_dict)

    return jsonify(products)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
