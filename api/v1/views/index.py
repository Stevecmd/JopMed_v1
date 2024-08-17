#!/usr/bin/python3
# """ Index """
# import models
# from models.addresses import Addresses
# from models.base_model import BaseModel
# from models.categories import Categories
# from models.comments import Comments
# from models.doctors import Doctors
# from models.file_uploads import File_Uploads
# from models.inventory import Inventory
# from models.order_items import Order_Items
# from models.orders import Orders
# from models.payment_information import Payment_Information
# from models.payments import Payments
# from models.product_categories import Product_Categories
# from models.products_tags import Product_Tags
# from models.products import Products
# from models.reviews import Reviews
# from models.roles import Roles
# from models.shipping_information import Shipping_Information
# from models.shipping_methods import Shipping_Methods
# from models.tags import Tags
# from models.users_roles import User_Roles
# from models.users import User
# from models import storage
# from api.v1.views import app_views
# from flask import Flask, jsonify, request, abort, render_template


# app = Flask(__name__)
# app.register_blueprint(app_views)

# @app_views.route('/status', methods=['GET'], strict_slashes=False)
# def status():
#     """ Status of API """
#     return jsonify({"status": "OK"})


# @app_views.route('/stats', methods=['GET'], strict_slashes=False)
# def number_objects():
#     """ Retrieves the number of each objects by type """
#     # classes = [Amenity, City, product, Review, State, User]
#     classes = { Addresses, BaseModel,
#             Categories,  Comments,
#             Doctors,  File_Uploads,
#             Inventory, Order_Items,
#             Orders, Payment_Information,
#             Payments, Product_Categories,
#             Product_Tags, Product_Tags,
#             Products, Products,
#             Reviews, Roles, Shipping_Information,
#             Shipping_Methods, Tags,
#             User_Roles, User }
#     names = ["Addresses", "BaseModel", "Categories", "Comments", "Doctors", "File_Uploads",
#              "Inventory", "Order_Items", "Orders", "Payment_Information", "Payments",
#              "Product_categories", "Product_Tags", "Product", "Products", "Products",
#              "Reviews", "Roles", "Shipping_Information", "Shipping_Methods", "Tags",
#              "User_Roles", "User"]

#     num_objs = {}
#     for i in range(len(classes)):
#         num_objs[names[i]] = storage.count(classes[i])

#     return jsonify(num_objs)


# @app_views.route('/product_search/', methods=['POST'], strict_slashes=False)
# def search_products():
#     """Returns a list of products based on the search criteria"""
#     if request.get_json() is None:
#         abort(400, description="Not a JSON")

#     data = request.get_json()

#     if not data or not len(data):
#         products = storage.all(product).values()
#         list_products = [product.to_dict() for product in products]
#         return jsonify(list_products)

#     # states = data.get('states', [])
#     # cities = data.get('cities', [])
#     # amenities = data.get('amenities', [])

#     list_products = []

#     # if states:
#     #     states_obj = [storage.get(State, s_id) for s_id in states]
#     #     for state in states_obj:
#     #         if state:
#     #             for city in state.cities:
#     #                 for product in city.products:
#     #                     list_products.append(product)

#     # if cities:
#     #     city_obj = [storage.get(City, c_id) for c_id in cities]
#     #     for city in city_obj:
#     #         if city:
#     #             for product in city.products:
#     #                 list_products.append(product)

#     # if amenities:
#     #     if not list_products:
#     #         list_products = storage.all(product).values()
#     #     amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
#     #     list_products = [product for product in list_products
#     #                    if all([am in product.amenities for am in amenities_obj])]

#     products = []
#     for product in list_products:
#         product_dict = product.to_dict()
#         user = storage.get(User, product.user_id)
#         product_dict['user'] = user.to_dict()
#         products.append(product_dict)

#     return jsonify(products)

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

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
from models import storage
from.. import app  
from flask import Flask, jsonify, request, abort, render_template
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns the status of the API """
    return jsonify({"status": "OK"})

# @app.route('/status', methods=['GET'], strict_slashes=False)
# def status():
#     """ Returns the status of the API """
#     return jsonify({"status": "OK"}) 
  
@app.route('/stats', methods=['GET'], strict_slashes=False)  
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = { Addresses, BaseModel,
            Categories,  Comments,
            Doctors,  File_Uploads,
            Inventory, Order_Items,
            Orders, Payment_Information,
            Payments, Product_Categories,
            Product_Tags, Product_Tags,
            Products, Products,
            Reviews, Roles, Shipping_Information,
            Shipping_Methods, Tags,
            User_Roles, User }
    names = ["Addresses", "BaseModel", "Categories", "Comments", "Doctors", "File_Uploads",
             "Inventory", "Order_Items", "Orders", "Payment_Information", "Payments",
             "Product_categories", "Product_Tags", "Product", "Products", "Products",
             "Reviews", "Roles", "Shipping_Information", "Shipping_Methods", "Tags",
             "User_Roles", "User"]

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

    # states = data.get('states', [])
    # cities = data.get('cities', [])
    # amenities = data.get('amenities', [])

    list_products = []

    # if states:
    #     states_obj = [storage.get(State, s_id) for s_id in states]
    #     for state in states_obj:
    #         if state:
    #             for city in state.cities:
    #                 for product in city.products:
    #                     list_products.append(product)

    # if cities:
    #     city_obj = [storage.get(City, c_id) for c_id in cities]
    #     for city in city_obj:
    #         if city:
    #             for product in city.products:
    #                 list_products.append(product)

    # if amenities:
    #     if not list_products:
    #         list_products = storage.all(product).values()
    #     amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
    #     list_products = [product for product in list_products
    #                    if all([am in product.amenities for am in amenities_obj])]

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
