#!/usr/bin/python3
""" Flask Application """

from datetime import datetime, timezone, timedelta
from models import storage
from models.users import User
from models.addresses import Addresses
from models.orders import Orders
from models.doctors import Doctors
from models.comments import Comments
from models.categories import Categories

from models.order_items import Order_Items
from models.payments import Payments
from models.payment_method import PaymentMethod
from models.product_categories import Product_Categories
from models.prescriptions import Prescriptions
from models.products import Products
from models.products_tags import Product_Tags
from models.product_images import Product_Images
from models.shipping_methods import Shipping_Methods
from models.shipping_information import Shipping_Information
from models.shopping_cart import ShoppingCart
from models.service import Service
from models.roles import Roles
from models.reviews import Reviews
from models.users_roles import User_Roles
from models.wishlist import Wishlist
import os
from os import environ
from flask import Flask, request, render_template, redirect, url_for, session, flash, make_response, send_file, request, jsonify
from flask import flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from api.v1.views import app_views
from sqlalchemy.exc import IntegrityError
import logging
import string
import random
from io import BytesIO
from reportlab.pdfgen import canvas
import models


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = 'jopmed_secret_key'
app.config['SESSION_COOKIE_SECURE'] = True  # for HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Set session to last for 7 days

cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)



@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

@app.route('/api/v1/status', methods=['GET'])
def status():
    """ Status of the API """
    return jsonify({"status": "OK"})

app.config['SWAGGER'] = {
    'title': 'JOPMED Restful API',
    'ui-version': 3
}

Swagger(app)


@app.before_request
def log_request_info():
    logging.debug('Headers: %s', request.headers)
    logging.debug('Body: %s', request.get_data())
    logging.debug('Session: %s', session)


# Authentication Routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            user_id = session['user_id']
            user = storage.get(User, user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Get the role ID for the required role
            role = storage.filter(Roles, name=role_name)
            if not role:
                return jsonify({'error': 'Role not found'}), 404
            role_id = role[0].id
            
            # Check if the user has the required role
            user_role = storage.filter(User_Roles, user_id=user_id, role_id=role_id)
            if not user_role:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Authentication and User Management
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = storage.session.query(User).filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        session['user_id'] = user.id
        session['username'] = user.username
        logging.info(f"User {user.id} logged in successfully")
        return jsonify({'success': True, 'user_id': user.id, 'username': user.username}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/api/logout', methods=['POST'])
def api_logout():
    try:
        session.clear()
        return jsonify({'success': True}), 200
    except Exception as e:
        app.logger.error(f"Failed to log out: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to log out'}), 500


@app.route('/api/register', methods=['PUT'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')

    if not all([username, email, first_name, last_name, password]):
        return jsonify({'error': 'All fields are required'}), 400

    # Check if the username or email already exists
    existing_user = storage.session.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 409

    # Create a new user
    password_hash = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password_hash=password_hash
    )

    try:
        storage.new(new_user)
        storage.save()
        return jsonify({'success': True, 'user_id': new_user.id, 'message': 'Registration successful'}), 201
    except IntegrityError:
        app.logger.error(f"Failed to register user: {str(e)}")
        return jsonify({'error': 'Failed to register user'}), 500

def get_current_user():
    if 'user_id' in session:
        return storage.get(User, session['user_id'])
    return None


@app.route('/api/account', methods=['GET'])
def account():
    user_id = request.headers.get('User-ID')
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/api/admin-only')
# @login_required
@role_required('admin')
def admin_only():
    return jsonify({'message': 'Welcome, admin!'})

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            user = storage.get(User, session['user_id'])
            if not user or user.role != role:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user = storage.get_by_email(User, data['email'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Generate a random password
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    user.password_hash = generate_password_hash(new_password)
    user.save()
    
    return jsonify({'message': 'Password reset', 'new_password': new_password}), 200

# User Routes
@app.route('/api/users', methods=['GET'])
# @login_required
def get_users():
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app.route('/api/users/<user_id>', methods=['GET'])
# @login_required
def get_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        logging.error(f"Invalid user ID: {user_id}")
        return not_found(404)

    logging.info(f"Fetching user with ID: {user_id}")
    user = storage.get(User, user_id)
    if not user:
        logging.error(f"User with ID {user_id} not found")
        return not_found(404)
    logging.info(f"User found: {user.to_dict()}")
    return jsonify(user.to_dict())


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)
    
    # Hash the password before saving the user
    password = data.pop('password', None)
    if password:
        data['password_hash'] = User().set_password(password)
    
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app.route('/api/users/<user_id>', methods=['PUT'])
# @login_required
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        return not_found(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)
    for key, value in data.items():
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())


@app.route('/api/users/<user_id>', methods=['DELETE'])
# @login_required
def delete_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        logging.error(f"Invalid user ID: {user_id}")
        return not_found(404)

    logging.info(f"Deleting user with ID: {user_id}")
    user = storage.get(User, user_id)
    if not user:
        logging.error(f"User with ID {user_id} not found")
        return not_found(404)

    user_details = user.to_dict()
    user.delete()
    storage.save()
    logging.info(f"User with ID {user_id} deleted")
    return make_response(jsonify(user_details), 200)


# Address Routes
@app.route('/api/addresses', methods=['GET'])
# @login_required
def get_addresses():
    addresses = storage.all(Addresses).values()
    return jsonify([address.to_dict() for address in addresses])


@app.route('/api/addresses/<address_id>', methods=['GET'])
# @login_required
def get_address(address_id):
    try:
        address_id = int(address_id)
    except ValueError:
        logging.error(f"Invalid address ID: {address_id}")
        return not_found(404)

    logging.info(f"Fetching address with ID: {address_id}")
    address = storage.get(Addresses, address_id)
    if not address:
        logging.error(f"Address with ID {address_id} not found")
        return not_found(404)

    logging.info(f"Address found: {address.to_dict()}")
    return jsonify(address.to_dict())


@app.route('/api/addresses', methods=['POST'])
# @login_required
def create_address():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)
    address = Addresses(**data)
    address.save()
    return make_response(jsonify(address.to_dict()), 201)


@app.route('/api/addresses/<address_id>', methods=['PUT'])
# @login_required
def update_address(address_id):
    try:
        address_id = int(address_id)
    except ValueError:
        logging.error(f"Invalid address ID: {address_id}")
        return not_found(404)

    address = storage.get(Addresses, address_id)
    if not address:
        logging.error(f"Address with ID {address_id} not found")
        return not_found(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)

    for key, value in data.items():
        setattr(address, key, value)
    address.save()
    return jsonify(address.to_dict())


@app.route('/api/addresses/<address_id>', methods=['DELETE'])
# @login_required
def delete_address(address_id):
    try:
        address_id = int(address_id)
    except ValueError:
        return not_found(404)

    logging.info(f"Deleting address with ID: {address_id}")
    address = storage.get(Addresses, address_id)
    if not address:
        return not_found(404)

    # Handle associated shipping_information records
    shipping_info_records = storage.all(Shipping_Information).values()
    for record in shipping_info_records:
        if record.address_id == address_id:
            record.delete()

    storage.save()

    address_details = address.to_dict()
    address.delete()
    storage.save()
    logging.info(f"Address with ID {address_id} deleted")
    return make_response(jsonify(address_details), 200)


# Order Routes
@app.route('/api/orders', methods=['GET'])
# @login_required
def get_orders():
    orders = storage.all(Orders).values()
    return jsonify([order.to_dict() for order in orders])


@app.route('/api/orders/<order_id>', methods=['GET'])
# @login_required
def get_order(order_id):
    logging.info(f"Fetching order with ID {order_id}")
    order = storage.get(Orders, order_id)
    if not order:
        logging.error(f"Order with ID {order_id} not found")
        return make_response(jsonify({'error': "Not found"}), 404)
    logging.info(f"Order with ID {order_id} found: {order.to_dict()}")
    return jsonify(order.to_dict())


@app.route('/api/orders', methods=['POST'])
# @login_required
def create_order():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)
    order = Orders(**data)
    order.save()
    return make_response(jsonify(order.to_dict()), 201)


@app.route('/api/orders/<order_id>', methods=['PUT'])
# @login_required
def update_order(order_id):
    order = storage.get(Orders, order_id)
    if not order:
        return make_response(jsonify({'error': "Not found"}), 404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for key, value in data.items():
        setattr(order, key, value)
    order.save()
    return jsonify(order.to_dict())


@app.route('/api/orders/<order_id>', methods=['DELETE'])
# @login_required
def delete_order(order_id):
    try:
        logging.info(f"Attempting to delete order with ID: {order_id}")
        
        order = storage.get(Orders, order_id)
        if not order:
            logging.warning(f"Order with ID {order_id} not found")
            return not_found(404)

        # Fetch and delete related payments
        payments = storage.all(Payments).values()
        related_payments = [payment for payment in payments if payment.order_id == order_id]
        for payment in related_payments:
            payment.delete()
        
        # Fetch and delete related order items
        order_items = storage.all(Order_Items).values()
        related_order_items = [item for item in order_items if item.order_id == order_id]
        for item in related_order_items:
            item.delete()
        
        storage.save()

        # Now delete the order
        order_details = order.to_dict()
        order.delete()
        storage.save()
        
        logging.info(f"Order with ID {order_id} deleted successfully")
        return make_response(jsonify(order_details), 200)
    except ValueError as ve:
        logging.error(f"ValueError while deleting order with ID {order_id}: {ve}")
        return not_found(404)
    except Exception as e:
        logging.error(f"Exception while deleting order with ID {order_id}: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)

# Order Items Routes
@app.route('/api/order_items', methods=['GET'])
def get_order_items():
    order_items = storage.all(Order_Items).values()
    return jsonify([order_item.to_dict() for order_item in order_items])

@app.route('/api/order_items/<order_item_id>', methods=['GET'])
def get_order_item(order_item_id):
    logging.info(f"Fetching order item with ID {order_item_id}")
    order_item = storage.get(Order_Items, order_item_id)
    if not order_item:
        return make_response(jsonify({'error': "Order item not found"}), 404)
    logging.info(f"Order item with ID {order_item_id} found: {order_item.to_dict()}")
    return jsonify(order_item.to_dict())

@app.route('/api/order_items', methods=['POST'])
def create_order_item():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    required_fields = ['order_id', 'product_id', 'quantity', 'price']
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({"error": f"Missing {field}"}), 400)
    
    order_item = Order_Items(**data)
    order_item.save()
    return make_response(jsonify(order_item.to_dict()), 201)

@app.route('/api/order_items/<order_item_id>', methods=['PUT'])
def update_order_item(order_item_id):
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    order_item = storage.get(Order_Items, order_item_id)
    if not order_item:
        return make_response(jsonify({'error': "Order item not found"}), 404)
    
    for key, value in data.items():
        if key in ['order_id', 'product_id', 'quantity', 'price']:
            setattr(order_item, key, value)
    
    order_item.save()
    return jsonify(order_item.to_dict())

@app.route('/api/order_items/<order_item_id>', methods=['DELETE'])
def delete_order_item(order_item_id):
    order_item = storage.get(Order_Items, order_item_id)
    if not order_item:
        return make_response(jsonify({'error': "Order item not found"}), 404)
    
    order_item.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Doctor Routes
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    doctors = storage.all(Doctors).values()
    return jsonify([doctor.to_dict() for doctor in doctors])


@app.route('/api/doctors/<doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = storage.get(Doctors, doctor_id)
    if not doctor:
        return not_found(404)
    return jsonify(doctor.to_dict())


@app.route('/api/doctors', methods=['POST'])
def create_doctor():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)
    
    required_fields = ['first_name', 'last_name', 'specialization', 'phone_number', 'email']
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({'error': f'Missing {field}'}), 400)
    
    # Check if email already exists
    existing_doctor = storage.get_by_email(Doctors, data['email'])
    if existing_doctor:
        return make_response(jsonify({'error': 'Email already exists'}), 400)
    
    doctor = Doctors(**data)
    doctor.save()
    return make_response(jsonify(doctor.to_dict()), 201)


@app.route('/api/doctors/<doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    doctor = storage.get(Doctors, doctor_id)
    if not doctor:
        return not_found(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)
    for key, value in data.items():
        setattr(doctor, key, value)
    doctor.save()
    return jsonify(doctor.to_dict())


@app.route('/api/doctors/<doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    doctor = storage.get(Doctors, doctor_id)
    if not doctor:
        return not_found(404)
    doctor.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Comment Routes
@app.route('/api/comments', methods=['GET'])
def get_comments():
    comments = storage.all(Comments).values()
    return jsonify([comment.to_dict() for comment in comments])


@app.route('/api/comments/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = storage.get(Comments, comment_id)
    if not comment:
        return make_response(jsonify({'error': "Not found"}), 404)
    return jsonify(comment.to_dict())


@app.route('/api/comments', methods=['POST'])
# @login_required
def create_comment():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    comment = Comments(**data)
    comment.save()
    return make_response(jsonify(comment.to_dict()), 201)


@app.route('/api/comments/<comment_id>', methods=['PUT'])
# @login_required
def update_comment(comment_id):
    comment = storage.get(Comments, comment_id)
    if not comment:
        return make_response(jsonify({'error': "Not found"}), 404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for key, value in data.items():
        setattr(comment, key, value)
    comment.save()
    return jsonify(comment.to_dict())


@app.route('/api/comments/<comment_id>', methods=['DELETE'])
# @login_required
def delete_comment(comment_id):
    comment = storage.get(Comments, comment_id)
    if not comment:
        return make_response(jsonify({'error': "Not found"}), 404)
    comment.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Categories Routes
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = storage.all(Categories).values()
    categories_list = [category.to_dict() for category in categories]
    return jsonify(categories_list)


@app.route('/api/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    category = storage.get(Categories, category_id)
    if not category:
        return make_response(jsonify({'error': "Not found"}), 404)
    return jsonify(category.to_dict())


@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    category = Categories(**data)
    category.save()
    return make_response(jsonify(category.to_dict()), 201)


@app.route('/api/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    category = storage.get(Categories, category_id)
    if not category:
        return make_response(jsonify({'error': "Not found"}), 404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for key, value in data.items():
        setattr(category, key, value)
    category.save()
    return jsonify(category.to_dict())


@app.route('/api/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category_id = int(category_id)
    except ValueError:
        return make_response(jsonify({'error': 'Invalid category ID'}), 400)

    category = storage.get(Categories, category_id)
    if not category:
        return make_response(jsonify({'error': 'Category not found'}), 404)
    
    category.delete()
    storage.save()
    return make_response(jsonify({'success': 'Category deleted'}), 200)


# Product Categories Routes
@app.route('/api/product_categories', methods=['GET'])
def get_product_categories():
    product_categories = storage.all(Product_Categories).values()
    return jsonify([pc.to_dict() for pc in product_categories])


@app.route('/api/product_categories/<product_id>', methods=['GET'])
def get_product_categories_by_product(product_id):
    try:
        product_id = int(product_id)
    except ValueError:
        return make_response(jsonify({'error': 'Invalid product ID'}), 400)

    product_categories = storage.filter(Product_Categories, product_id=product_id)
    if not product_categories:
        return make_response(jsonify({'error': 'Product categories not found'}), 404)

    return jsonify([category.to_dict() for category in product_categories])


@app.route('/api/product_categories', methods=['POST'])
# @login_required
def create_product_category():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'product_id' not in data or 'category_id' not in data:
        return make_response(
            jsonify({
                'error': 'Missing product_id or category_id'
                }), 400)
    new_pc = Product_Categories(**data)
    try:
        new_pc.save()
    except IntegrityError:
        return make_response(jsonify({'error': 'Invalid product_id or category_id'}), 400)
    return jsonify(new_pc.to_dict()), 201


@app.route(
    '/api/product_categories/<product_id>/<category_id>',
    methods=['DELETE']
)
# @login_required
def delete_product_category(product_id, category_id):
    pc = storage.get(Product_Categories, (product_id, category_id))
    if not pc:
        return not_found(404)
    deleted_content = pc.to_dict()
    storage.delete(pc)
    storage.save()
    print(deleted_content)
    return jsonify({}), 200


# Prescriptions Routes!
@app.route('/api/prescriptions', methods=['GET'])
# @login_required
def get_prescriptions():
    """Retrieve all prescriptions"""
    prescriptions = storage.all(Prescriptions).values()
    return jsonify([prescription.to_dict() for prescription in prescriptions])


@app.route('/api/prescriptions/<prescription_id>', methods=['GET'])
# @login_required
def get_prescription(prescription_id):
    """Retrieve a specific prescription by ID"""
    prescription = storage.get(Prescriptions, prescription_id)
    if not prescription:
        return make_response(jsonify({'error': "Not found"}), 404)
    return jsonify(prescription.to_dict())


@app.route('/api/prescriptions', methods=['POST'])
# @login_required
def create_prescription():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    required_fields = ['user_id', 'doctor_id', 'medication', 'dosage', 'instructions']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return make_response(jsonify({'error': f"Missing fields: {', '.join(missing_fields)}"}), 400)
    
    prescription = Prescriptions(**data)
    storage.new(prescription)
    storage.save()
    return make_response(jsonify(prescription.to_dict()), 201)


@app.route('/api/prescriptions/<prescription_id>', methods=['DELETE'])
# @login_required
def delete_prescription(prescription_id):
    prescription = storage.get(Prescriptions, prescription_id)
    if not prescription:
        return not_found(404)
    deleted_content = prescription.to_dict()
    prescription.delete()
    storage.save()
    return jsonify(deleted_content), 200


@app.route('/api/prescriptions/<prescription_id>', methods=['PUT'])
# @login_required
def update_prescription(prescription_id):
    """Update a prescription by ID"""
    logging.debug(f"Attempting to update prescription with ID: {prescription_id}")
    
    prescription = storage.get(Prescriptions, prescription_id)
    if not prescription:
        logging.error(f"Prescription with ID {prescription_id} not found")
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    data = request.get_json()
    if not data:
        logging.error("Request data is not a valid JSON")
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    
    # Update the prescription fields
    for key, value in data.items():
        if key in ['user_id', 'doctor_id', 'medication', 'dosage', 'instructions', 'prescription_date', 'expiration_date']:
            setattr(prescription, key, value)
    
    prescription.save()
    logging.debug(f"Prescription with ID {prescription_id} updated successfully")
    return jsonify(prescription.to_dict())


# Products Routes
@app.route('/api/products', methods=['GET'])
def get_products():
    products = storage.all(Products).values()
    return jsonify([product.to_dict(include_image=True) for product in products])


@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = storage.get(Products, product_id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(product.to_dict())


@app.route('/api/products', methods=['POST'])
# @login_required
def create_product():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data or 'price' not in data or 'stock' not in data:
        return make_response(
            jsonify({
                'error': 'Missing name, price or stock'
            }), 400)
    new_product = Products(**data)
    new_product.save()
    return make_response(jsonify(new_product.to_dict()), 201)


@app.route('/api/products/<product_id>', methods=['PUT'])
# @login_required
def update_product(product_id):
    product = storage.get(Products, product_id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(product, key, value)
    product.save()
    return make_response(jsonify(product.to_dict()), 200)


@app.route('/api/products/<product_id>', methods=['DELETE'])
# @login_required
def delete_product(product_id):
    product = storage.get(Products, product_id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    product.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app.route('/api/products/<product_id>/rate', methods=['POST'])
def rate_product(product_id):
    logging.info(f"Attempting to rate product {product_id}")
    logging.info(f"Session contents: {session}")

    # Check if product exists
    if product_id == 'undefined':
        return jsonify({'error': 'Invalid product ID'}), 400

    # Check if user is logged in
    if 'user_id' not in session:
        logging.warning("User not logged in")
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']
    logging.info(f"User ID from session: {user_id}")

    product = storage.get(Products, product_id)
    if not product:
        logging.warning(f"Product {product_id} not found")
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json()
    logging.info(f"Received data: {data}")
    if not data or 'rating' not in data:
        logging.warning("Missing rating in request data")
        return jsonify({'error': 'Missing rating'}), 400

    rating = int(data['rating'])
    if rating < 1 or rating > 5:
        logging.warning(f"Invalid rating: {rating}")
        return jsonify({'error': 'Invalid rating'}), 400

    # Check if the user has already rated this product
    existing_review = storage.filter(Reviews, user_id=user_id, product_id=product_id)
    if existing_review:
        existing_review = existing_review[0]  # Get the first (and should be only) review
        existing_review.rating = rating
        existing_review.updated_at = datetime.now(timezone.utc)
        logging.info(f"Updated existing review for user {user_id} on product {product_id}")
    else:
        new_review = Reviews(user_id=user_id, product_id=product_id, rating=rating)
        storage.new(new_review)
        logging.info(f"Created new review for user {user_id} on product {product_id}")
    
    storage.save()

    new_average = calculate_average_rating(product_id)
    logging.info(f"New average rating for product {product_id}: {new_average}")

    return jsonify({
        'success': True,
        'new_average': new_average
    }), 201


@app.route('/api/products/<product_id>/comments', methods=['GET'])
def get_product_comments(product_id):
    product = storage.get(Products, product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    comments = [comment.to_dict() for comment in product.comments]
    return jsonify({
        'product_name': product.name,
        'comments': comments
    })

@app.route('/api/products/<product_id>/comments', methods=['POST'])
def add_product_comment(product_id):
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    product = storage.get(Products, product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'Missing comment content'}), 400

    new_comment = Comments(
        user_id=session['user_id'],
        product_id=product_id,
        content=data['content']
    )
    storage.new(new_comment)
    storage.save()

    return jsonify(new_comment.to_dict()), 201


def calculate_average_rating(product_id):
    reviews = storage.filter(Reviews, product_id=product_id)
    if not reviews:
        return 0
    total_rating = sum(review.rating for review in reviews)
    return total_rating / len(reviews)


# Product Tags Routes
@app.route('/api/product_tags', methods=['GET'])
def get_product_tags():
    """Retrieve all product tags"""
    product_tags = storage.all(Product_Tags).values()
    product_tags_list = [tag.to_dict() for tag in product_tags]
    return jsonify(product_tags_list)


@app.route('/api/product_tags/<product_id>', methods=['GET'])
def get_product_tags_by_product(product_id):
    product_tags = storage.filter(Product_Tags, product_id=product_id)
    return jsonify([pt.to_dict() for pt in product_tags])


@app.route('/api/product_tags', methods=['POST'])
# @login_required
def create_product_tag():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'product_id' not in data or 'tag_id' not in data:
        return make_response(
            jsonify({
                'error': 'Missing product_id or tag_id'}), 400)
    new_pt = Product_Tags(**data)
    new_pt.save()
    return make_response(jsonify(new_pt.to_dict()), 201)


@app.route('/api/product_tags/<product_id>/<tag_id>', methods=['DELETE'])
# @login_required
def delete_product_tag(product_id, tag_id):
    pt = storage.get(Product_Tags, (product_id, tag_id))
    if not pt:
        return make_response(jsonify({'error': 'Not found'}), 404)
    pt.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Product Images Routes
@app.route('/api/product_images', methods=['GET'])
def get_product_images():
    logging.info("Fetching all product images")
    product_images = storage.all(Product_Images).values()
    if not product_images:
        logging.info("No product images found")
    response = jsonify([pi.to_dict() for pi in product_images])
    logging.info(f"Response: {response.get_json()}")
    return response


@app.route('/api/product_images/<product_id>', methods=['GET'])
# @login_required
def get_product_images_by_product(product_id):
    logging.info(f"Fetching product images for product ID: {product_id}")
    product_images = storage.all(Product_Images).values()
    if not product_images:
        logging.info("No product images found")
    filtered_images = [pi.to_dict() for pi in product_images if pi.product_id == int(product_id)]
    if not filtered_images:
        logging.info(f"No product images found for product ID: {product_id}")
    response = jsonify(filtered_images)
    logging.info(f"Response: {response.get_json()}")
    return response


@app.route('/api/product_images', methods=['POST'])
def create_product_image():
    data = request.get_json()
    if not data:
        response = make_response(jsonify({'error': 'Not a JSON'}), 400)
        print(response.get_json())
        return response
    if 'product_id' not in data or 'image_url' not in data:
        response = make_response(
            jsonify({
                'error': 'Missing product_id or image_url'
            }),
            400
        )
        print(response.get_json())
        return response
    new_pi = Product_Images(**data)
    new_pi.save()
    response = make_response(jsonify(new_pi.to_dict()), 201)
    print(response.get_json())
    return response


@app.route('/api/product_images/<image_id>', methods=['DELETE'])
# @login_required
def delete_product_image(image_id):
    pi = storage.get(Product_Images, image_id)
    if not pi:
        response = make_response(jsonify({'error': 'Not found'}), 404)
        print(response.get_json())
        return response
    pi.delete()
    storage.save()
    response = make_response(jsonify({}), 200)
    print(response.get_json())
    return response


# Shipping Methods Routes
@app.route('/api/shipping_methods', methods=['GET'])
# @login_required
def get_shipping_methods():
    shipping_methods = storage.all(Shipping_Methods).values()
    return jsonify([method.to_dict() for method in shipping_methods])


@app.route('/api/shipping_methods/<method_id>', methods=['GET'])
# @login_required
def get_shipping_method(method_id):
    method = storage.get(Shipping_Methods, method_id)
    if not method:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(method.to_dict())


@app.route('/api/shipping_methods', methods=['POST'])
# @login_required
def create_shipping_method():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_method = Shipping_Methods(**data)
    new_method.save()
    return make_response(jsonify(new_method.to_dict()), 201)


@app.route('/api/shipping_methods/<method_id>', methods=['PUT'])
# @login_required
def update_shipping_method(method_id):
    method = storage.get(Shipping_Methods, method_id)
    if not method:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        setattr(method, key, value)
    method.save()
    return make_response(jsonify(method.to_dict()), 200)


@app.route('/api/shipping_methods/<method_id>', methods=['DELETE'])
# @login_required
def delete_shipping_method(method_id):
    method = storage.get(Shipping_Methods, method_id)
    if not method:
        return make_response(jsonify({'error': 'Not found'}), 404)
    method.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Shipping Information Routes
@app.route('/api/shipping_information', methods=['GET'])
def get_shipping_information():
    shipping_info = storage.all(Shipping_Information).values()
    return jsonify([info.to_dict() for info in shipping_info])


@app.route('/api/shipping_information/<info_id>', methods=['GET'])
def get_shipping_info(info_id):
    info = storage.get(Shipping_Information, info_id)
    if not info:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(info.to_dict())


@app.route('/api/shipping_information', methods=['POST'])
def create_shipping_info():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if (
        'user_id' not in data or
        'address_id' not in data or
        'shipping_method_id' not in data
    ):
        return make_response(
            jsonify({
                'error': 'Missing user_id, address_id or shipping_method_id'
            }),
            400
        )
    new_info = Shipping_Information(**data)
    new_info.save()
    return make_response(jsonify(new_info.to_dict()), 201)


@app.route('/api/shipping_information/<info_id>', methods=['PUT'])
def update_shipping_info(info_id):
    info = storage.get(Shipping_Information, info_id)
    if not info:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        setattr(info, key, value)
    info.save()
    return make_response(jsonify(info.to_dict()), 200)


@app.route('/api/shipping_information/<info_id>', methods=['DELETE'])
def delete_shipping_info(info_id):
    info = storage.get(Shipping_Information, info_id)
    if not info:
        return make_response(jsonify({'error': 'Not found'}), 404)
    info.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Roles Routes
@app.route('/api/roles', methods=['GET'])
def get_roles():
    roles = storage.all(Roles).values()
    return jsonify([role.to_dict() for role in roles])


@app.route('/api/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    role = storage.get(Roles, role_id)
    if not role:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(role.to_dict())


@app.route('/api/roles', methods=['POST'])
# @login_required
def create_role():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_role = Roles(**data)
    new_role.save()
    return make_response(jsonify(new_role.to_dict()), 201)


@app.route('/api/roles/<int:role_id>', methods=['PUT'])
# @login_required
def update_role(role_id):
    role = storage.get(Roles, role_id)
    if not role:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        setattr(role, key, value)
    role.save()
    return make_response(jsonify(role.to_dict()), 200)


@app.route('/api/roles/<int:role_id>', methods=['DELETE'])
# @login_required
def delete_role(role_id):
    role = storage.get(Roles, role_id)
    if not role:
        return make_response(jsonify({'error': 'Not found'}), 404)
    role.delete()
    storage.save()
    return make_response(jsonify({}), 200)

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user or user.role != role:
                return jsonify({'error': 'Unauthorized'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Reviews Routes
# Read All Reviews:
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = storage.all(Reviews).values()
    return jsonify([review.to_dict() for review in reviews])


# Read a Single Review:
@app.route('/api/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Reviews, review_id)
    if not review:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(review.to_dict())


# Create a Review:
@app.route('/api/reviews', methods=['POST'])
# @login_required
def create_review():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if (
        'user_id' not in data or
        'product_id' not in data or
        'rating' not in data
    ):
        return make_response(
            jsonify({'error': 'Missing user_id, product_id or rating'}),
            400
        )
    new_review = Reviews(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


# Update a Review:
@app.route('/api/reviews/<review_id>', methods=['PUT'])
# @login_required
def update_review(review_id):
    review = storage.get(Reviews, review_id)
    if not review:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)


# Delete a Review:
@app.route('/api/reviews/<review_id>', methods=['DELETE'])
# @login_required
def delete_review(review_id):
    review = storage.get(Reviews, review_id)
    if not review:
        return make_response(jsonify({'error': 'Not found'}), 404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Payment Routes
# Create a Payment
@app.route('/api/payment', methods=['POST'])
# @login_required
def initiate_payment():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'order_id' not in data or 'amount' not in data:
        return make_response(jsonify({'error': 'Missing order_id or amount'}), 400)
    
    order = storage.get(Orders, data['order_id'])
    if not order:
        return make_response(jsonify({'error': 'Order not found'}), 404)
    
    new_payment = Payments(
        order_id=data['order_id'],
        payment_status='pending',
        amount=data['amount'],
        transaction_id=data.get('transaction_id', ''),
        payment_date=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    new_payment.save()
    return make_response(jsonify(new_payment.to_dict()), 201)

# Read All Payments
@app.route('/api/payments', methods=['GET'])
# @login_required
def get_payments():
    payments = storage.all(Payments).values()
    return jsonify([payment.to_dict() for payment in payments])

# Read a Single Payment
@app.route('/api/payments/<payment_id>', methods=['GET'])
# @login_required
def get_payment(payment_id):
    payment = storage.get(Payments, payment_id)
    if not payment:
        return make_response(jsonify({'error': 'Payment not found'}), 404)
    return jsonify(payment.to_dict())

# Update a Payment
@app.route('/api/payments/<payment_id>', methods=['PUT'])
# @login_required
def update_payment(payment_id):
    payment = storage.get(Payments, payment_id)
    if not payment:
        return make_response(jsonify({'error': 'Payment not found'}), 404)
    
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    
    for key, value in data.items():
        if key in ['order_id', 'payment_status', 'amount', 'transaction_id']:
            setattr(payment, key, value)
    payment.updated_at = datetime.utcnow()
    payment.save()
    return jsonify(payment.to_dict())

# Delete a Payment
@app.route('/api/payments/<payment_id>', methods=['DELETE'])
# @login_required
def delete_payment(payment_id):
    payment = storage.get(Payments, payment_id)
    if not payment:
        return make_response(jsonify({'error': 'Payment not found'}), 404)
    
    payment.delete()
    storage.save()
    return make_response(jsonify({}), 200)

# Confirm a Payment
@app.route('/api/payment/confirm', methods=['POST'])
# @login_required
def confirm_payment():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'payment_id' not in data or 'payment_status' not in data:
        return make_response(jsonify({'error': 'Missing payment_id or payment_status'}), 400)
    
    payment = storage.get(Payments, data['payment_id'])
    if not payment:
        return make_response(jsonify({'error': 'Payment not found'}), 404)
    
    payment.payment_status = data['payment_status']
    payment.updated_at = datetime.utcnow()
    payment.save()
    return make_response(jsonify(payment.to_dict()), 200)


@app.route('/api/services', methods=['GET'])
def get_services():
    services = storage.all(Service).values()
    return jsonify([service.to_dict() for service in services])

@app.route('/api/services/<service_id>', methods=['GET'])
def get_service(service_id):
    service = storage.get(Service, service_id)
    if not service:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(service.to_dict())

@app.route('/api/services', methods=['POST'])
def create_service():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    required_fields = ['name', 'description', 'price', 'user_id', 'order_id']
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({'error': f'Missing {field}'}), 400)
    new_service = Service(**data)
    new_service.save()
    return make_response(jsonify(new_service.to_dict()), 201)

@app.route('/api/services/<service_id>', methods=['PUT'])
def update_service(service_id):
    service = storage.get(Service, service_id)
    if not service:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(service, key, value)
    service.save()
    return jsonify(service.to_dict())

@app.route('/api/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = storage.get(Service, service_id)
    if not service:
        return make_response(jsonify({'error': 'Not found'}), 404)
    service.delete()
    storage.save()
    return make_response(jsonify({}), 200)

# Wishlist Routes
@app.route('/api/wishlist', methods=['GET'])
def view_wishlist():
    user_id = request.headers.get('User-ID')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    wishlist_items = storage.filter(Wishlist, user_id=user_id)
    return jsonify([item.to_dict() for item in wishlist_items])

@app.route('/api/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.get_json()
    if not data or 'user_id' not in data or 'item_name' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    new_item = Wishlist(**data)
    new_item.save()
    return jsonify({'message': 'Item added to wishlist', 'item': new_item.to_dict()}), 201

@app.route('/api/wishlist', methods=['PUT'])
def update_wishlist():
    data = request.get_json()
    if not data or 'id' not in data or 'user_id' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    item = storage.get(Wishlist, data['id'])
    if not item or str(item.user_id) != str(data['user_id']):
        return jsonify({'error': 'Item not found or unauthorized'}), 404

    for key, value in data.items():
        if key != 'id' and key != 'user_id':
            setattr(item, key, value)
    item.save()
    return jsonify({'message': 'Item updated in wishlist', 'item': item.to_dict()}), 200

@app.route('/api/wishlist', methods=['DELETE'])
def remove_from_wishlist():
    data = request.get_json()
    if not data or 'id' not in data or 'user_id' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    item = storage.get(Wishlist, data['id'])
    if not item or str(item.user_id) != str(data['user_id']):
        return jsonify({'error': 'Item not found or unauthorized'}), 404

    item.delete()
    storage.save()
    return jsonify({'message': 'Item removed from wishlist'}), 200

# Shopping Cart Routes
@app.route('/api/cart', methods=['GET'])
def get_cart():
    user_id = request.headers.get('User-ID')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    cart_items = storage.session.query(ShoppingCart).filter_by(user_id=user_id).all()
    return jsonify([item.to_dict() for item in cart_items])

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    service_id = data.get('service_id')
    quantity = data.get('quantity', 1)

    if not user_id or not (product_id or service_id) or not quantity:
        return jsonify({'error': 'Invalid data'}), 400

    cart_item = ShoppingCart(user_id=user_id, product_id=product_id, service_id=service_id, quantity=quantity)
    storage.new(cart_item)
    storage.save()
    return jsonify(cart_item.to_dict()), 201

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    item_id = data.get('item_id')
    quantity = data.get('quantity')

    if not user_id or not item_id or quantity is None:
        return jsonify({'error': 'Invalid data'}), 400

    cart_item = storage.session.query(ShoppingCart).filter_by(id=item_id, user_id=user_id).first()
    if not cart_item:
        return jsonify({'error': 'Item not found'}), 404

    cart_item.quantity = quantity
    storage.save()
    return jsonify(cart_item.to_dict()), 200

@app.route('/api/cart/remove', methods=['DELETE'])
def remove_from_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    item_id = data.get('item_id')

    if not user_id or not item_id:
        return jsonify({'error': 'Invalid data'}), 400

    cart_item = storage.session.query(ShoppingCart).filter_by(id=item_id, user_id=user_id).first()
    if not cart_item:
        return jsonify({'error': 'Item not found'}), 404

    storage.delete(cart_item)
    storage.save()
    return jsonify({'success': True}), 200

# Star Ratings
@app.route('/api/user/ratings', methods=['GET'])
def get_user_ratings():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    
    user_id = session['user_id']
    try:
        # Fetch user ratings directly from the database
        user_ratings = storage.filter(Reviews, user_id=user_id)
        
        # Convert the ratings to a dictionary format
        ratings_dict = {str(rating.product_id): rating.rating for rating in user_ratings}
        
        return jsonify(ratings_dict), 200
    except Exception as e:
        app.logger.error(f"Error fetching user ratings: {str(e)}")
        return jsonify({'error': 'Failed to fetch user ratings'}), 500



@app.route('/api/register-payment-method', methods=['POST'])
def register_payment_method():
    data = request.get_json()
    if not data or 'user_id' not in data or 'payment_method' not in data:
        return jsonify({'error': 'Invalid data. Please provide user_id and payment_method.'}), 400

    user_id = data['user_id']
    payment_method_data = data['payment_method']

    user = storage.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    payment_method = PaymentMethod(
        user_id=user_id,
        card_number=payment_method_data.get('card_number'),
        card_expiry=payment_method_data.get('card_expiry'),
        card_cvv=payment_method_data.get('card_cvv'),
        card_holder_name=payment_method_data.get('card_holder_name')
    )

    storage.new(payment_method)
    storage.save()
    return jsonify({'success': True, 'message': 'Payment method registered successfully'}), 201

@app.route('/api/purchase/confirm', methods=['POST'])
def confirm_purchase():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    
    user_id = session['user_id']
    cart_items = storage.filter(ShoppingCart, user_id=user_id)
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    total_amount = sum(item.product.price * item.quantity for item in cart_items if item.product)
    total_amount += sum(item.service.price * item.quantity for item in cart_items if item.service)
    
    # Create order
    new_order = Orders(
        user_id=user_id,
        address_id=1,  # You might want to get this from the user's default address or session
        status='pending',
        payment_method='credit_card',  # Adjust based on actual payment method used
        total_amount=total_amount
    )
    storage.new(new_order)
    
    # Create order items
    for cart_item in cart_items:
        if cart_item.product:
            order_item = Order_Items(
                order_id=new_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        else:
            order_item = Order_Items(
                order_id=new_order.id,
                service_id=cart_item.service_id,
                quantity=cart_item.quantity,
                price=cart_item.service.price
            )
        storage.new(order_item)
    
    # Clear cart
    for item in cart_items:
        storage.delete(item)
    
    storage.save()
    
    # Generate receipt
    receipt_url = url_for('generate_receipt', order_id=new_order.id)
    
    return jsonify({'success': True, 'receipt_url': receipt_url}), 200

@app.route('/api/receipt/<int:order_id>')
def generate_receipt(order_id):
    order = storage.get(Orders, order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # Add receipt content
    p.drawString(100, 750, f"Order Receipt #{order.id}")
    p.drawString(100, 700, f"Total Amount: ${order.total_amount:.2f}")
    p.drawString(100, 650, f"Date: {order.created_at}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"receipt_{order.id}.pdf", mimetype='application/pdf')


@app.route('/api/check_login', methods=['GET'])
def check_login():
    logged_in = 'user_id' in session
    user_id = session.get('user_id')
    username = session.get('username')
    print(f"Session contents: {session}")
    print(f"User logged in: {logged_in}, User ID: {user_id}, Username: {username}")
    return jsonify({'logged_in': logged_in, 'user_id': user_id, 'username': username})

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('JOPMED_API_HOST')
    port = environ.get('JOPMED_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True, debug=True)

