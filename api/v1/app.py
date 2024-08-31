#!/usr/bin/python3
""" Flask Application """
from api.v1.views import app_views
from models import storage
from models.users import User
from models.addresses import Addresses
from models.orders import Orders
from models.doctors import Doctors
from models.comments import Comments
from models.categories import Categories
from models.order_items import Order_Items
from models.payments import Payments
from models.product_categories import Product_Categories
from models.prescriptions import Prescriptions
from models.products import Products
from models.products_tags import Product_Tags
from models.product_images import Product_Images
from models.shipping_methods import Shipping_Methods
from models.shipping_information import Shipping_Information
from models.roles import Roles
from models.reviews import Reviews
from os import environ
from flask import Flask, request, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from api.v1.views import app_views
import logging
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

cors = CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(level=logging.INFO)

app.register_blueprint(app_views)

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

@app.route('/', strict_slashes=False)
@app.route('/jopmed-home', strict_slashes=False)
def jopmed():
    return "Home"


# User Routes
@app.route('/users', methods=['GET'])
def get_users():
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


# @app.route('/users/<user_id>', methods=['GET'])
# def get_user(user_id):
#     user = storage.get(User, user_id)
#     if not user:
#         return not_found(404)
#     return jsonify(user.to_dict())
@app.route('/users/<user_id>', methods=['GET'])
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


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app.route('/users/<user_id>', methods=['PUT'])
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


@app.route('/users/<user_id>', methods=['DELETE'])
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
@app.route('/addresses', methods=['GET'])
def get_addresses():
    addresses = storage.all(Addresses).values()
    return jsonify([address.to_dict() for address in addresses])


@app.route('/addresses/<address_id>', methods=['GET'])
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


@app.route('/addresses', methods=['POST'])
def create_address():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)
    address = Addresses(**data)
    address.save()
    return make_response(jsonify(address.to_dict()), 201)


@app.route('/addresses/<address_id>', methods=['PUT'])
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


@app.route('/addresses/<address_id>', methods=['DELETE'])
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
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = storage.all(Orders).values()
    return jsonify([order.to_dict() for order in orders])


@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    logging.info(f"Fetching order with ID {order_id}")
    order = storage.get(Orders, order_id)
    if not order:
        logging.error(f"Order with ID {order_id} not found")
        return make_response(jsonify({'error': "Not found"}), 404)
    logging.info(f"Order with ID {order_id} found: {order.to_dict()}")
    return jsonify(order.to_dict())


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)
    order = Orders(**data)
    order.save()
    return make_response(jsonify(order.to_dict()), 201)


@app.route('/orders/<order_id>', methods=['PUT'])
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


@app.route('/orders/<order_id>', methods=['DELETE'])
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
@app.route('/order_items', methods=['POST'])
def create_order_item():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)
    
    required_fields = ['order_id', 'product_id', 'quantity', 'price']
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({'error': f'Missing {field}'}), 400)
    
    order_item = Order_Items(**data)
    order_item.save()
    return make_response(jsonify(order_item.to_dict()), 201)


# Doctor Routes
@app.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = storage.all(Doctors).values()
    return jsonify([doctor.to_dict() for doctor in doctors])


@app.route('/doctors/<doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = storage.get(Doctors, doctor_id)
    if not doctor:
        return not_found(404)
    return jsonify(doctor.to_dict())


@app.route('/doctors', methods=['POST'])
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


@app.route('/doctors/<doctor_id>', methods=['PUT'])
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


@app.route('/doctors/<doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    doctor = storage.get(Doctors, doctor_id)
    if not doctor:
        return not_found(404)
    doctor.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Comment Routes
@app.route('/comments', methods=['GET'])
def get_comments():
    comments = storage.all(Comments).values()
    return jsonify([comment.to_dict() for comment in comments])


@app.route('/comments/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = storage.get(Comments, comment_id)
    if not comment:
        return make_response(jsonify({'error': "Not found"}), 404)
    return jsonify(comment.to_dict())


@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    comment = Comments(**data)
    comment.save()
    return make_response(jsonify(comment.to_dict()), 201)


@app.route('/comments/<comment_id>', methods=['PUT'])
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


@app.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = storage.get(Comments, comment_id)
    if not comment:
        return make_response(jsonify({'error': "Not found"}), 404)
    comment.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Category Routes
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = storage.all(Categories).values()
    return jsonify([category.to_dict() for category in categories])


@app.route('/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    category = storage.get(Categories, category_id)
    if not category:
        return make_response(jsonify({'error': "Not found"}), 404)
    return jsonify(category.to_dict())


@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    category = Categories(**data)
    category.save()
    return make_response(jsonify(category.to_dict()), 201)


@app.route('/categories/<category_id>', methods=['PUT'])
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


@app.route('/categories/<category_id>', methods=['DELETE'])
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
@app.route('/product_categories', methods=['GET'])
def get_product_categories():
    product_categories = storage.all(Product_Categories).values()
    return jsonify([pc.to_dict() for pc in product_categories])


@app.route('/product_categories/<product_id>', methods=['GET'])
def get_product_categories_by_product(product_id):
    try:
        product_id = int(product_id)
    except ValueError:
        return make_response(jsonify({'error': 'Invalid product ID'}), 400)

    product_categories = storage.filter(Product_Categories, product_id=product_id)
    if not product_categories:
        return make_response(jsonify({'error': 'Product categories not found'}), 404)

    return jsonify([category.to_dict() for category in product_categories])


@app.route('/product_categories', methods=['POST'])
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
    '/product_categories/<product_id>/<category_id>',
    methods=['DELETE']
)
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
@app.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    """Retrieve all prescriptions"""
    prescriptions = storage.all(Prescriptions).values()
    return jsonify([prescription.to_dict() for prescription in prescriptions])


@app.route('/prescriptions/<prescription_id>', methods=['GET'])
def get_prescription(prescription_id):
    """Retrieve a specific prescription by ID"""
    prescription = storage.get(Prescriptions, prescription_id)
    if not prescription:
        return make_response(jsonify({'error': "Not found"}), 404)
    return jsonify(prescription.to_dict())


@app.route('/prescriptions', methods=['POST'])
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


@app.route('/prescriptions/<prescription_id>', methods=['DELETE'])
def delete_prescription(prescription_id):
    prescription = storage.get(Prescriptions, prescription_id)
    if not prescription:
        return not_found(404)
    deleted_content = prescription.to_dict()
    prescription.delete()
    storage.save()
    return jsonify(deleted_content), 200


@app.route('/prescriptions/<prescription_id>', methods=['PUT'])
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
@app.route('/products', methods=['GET'])
def get_products():
    products = storage.all(Products).values()
    return jsonify([product.to_dict() for product in products])


@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = storage.get(Products, product_id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(product.to_dict())


@app.route('/products', methods=['POST'])
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


@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    product = storage.get(Products, product_id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        setattr(product, key, value)
    product.save()
    return make_response(jsonify(product.to_dict()), 200)


@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = storage.get(Products, product_id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    product.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Product Tags Routes
@app.route('/product_tags', methods=['GET'])
def get_product_tags():
    """Retrieve all product tags"""
    product_tags = storage.all(Product_Tags).values()
    product_tags_list = [tag.to_dict() for tag in product_tags]
    return jsonify(product_tags_list)


@app.route('/product_tags/<product_id>', methods=['GET'])
def get_product_tags_by_product(product_id):
    product_tags = storage.filter(Product_Tags, product_id=product_id)
    return jsonify([pt.to_dict() for pt in product_tags])


@app.route('/product_tags', methods=['POST'])
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


@app.route('/product_tags/<product_id>/<tag_id>', methods=['DELETE'])
def delete_product_tag(product_id, tag_id):
    pt = storage.get(Product_Tags, (product_id, tag_id))
    if not pt:
        return make_response(jsonify({'error': 'Not found'}), 404)
    pt.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Product Images Routes
@app.route('/product_images', methods=['GET'])
def get_product_images():
    logging.info("Fetching all product images")
    product_images = storage.all(Product_Images).values()
    if not product_images:
        logging.info("No product images found")
    response = jsonify([pi.to_dict() for pi in product_images])
    logging.info(f"Response: {response.get_json()}")
    return response


@app.route('/product_images/<product_id>', methods=['GET'])
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


@app.route('/product_images', methods=['POST'])
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


@app.route('/product_images/<image_id>', methods=['DELETE'])
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
@app.route('/shipping_methods', methods=['GET'])
def get_shipping_methods():
    shipping_methods = storage.all(Shipping_Methods).values()
    return jsonify([method.to_dict() for method in shipping_methods])


@app.route('/shipping_methods/<method_id>', methods=['GET'])
def get_shipping_method(method_id):
    method = storage.get(Shipping_Methods, method_id)
    if not method:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(method.to_dict())


@app.route('/shipping_methods', methods=['POST'])
def create_shipping_method():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_method = Shipping_Methods(**data)
    new_method.save()
    return make_response(jsonify(new_method.to_dict()), 201)


@app.route('/shipping_methods/<method_id>', methods=['PUT'])
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


@app.route('/shipping_methods/<method_id>', methods=['DELETE'])
def delete_shipping_method(method_id):
    method = storage.get(Shipping_Methods, method_id)
    if not method:
        return make_response(jsonify({'error': 'Not found'}), 404)
    method.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Shipping Information Routes
@app.route('/shipping_information', methods=['GET'])
def get_shipping_information():
    shipping_info = storage.all(Shipping_Information).values()
    return jsonify([info.to_dict() for info in shipping_info])


@app.route('/shipping_information/<info_id>', methods=['GET'])
def get_shipping_info(info_id):
    info = storage.get(Shipping_Information, info_id)
    if not info:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(info.to_dict())


@app.route('/shipping_information', methods=['POST'])
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


@app.route('/shipping_information/<info_id>', methods=['PUT'])
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


@app.route('/shipping_information/<info_id>', methods=['DELETE'])
def delete_shipping_info(info_id):
    info = storage.get(Shipping_Information, info_id)
    if not info:
        return make_response(jsonify({'error': 'Not found'}), 404)
    info.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Roles Routes
@app.route('/roles', methods=['GET'])
def get_roles():
    roles = storage.all(Roles).values()
    return jsonify([role.to_dict() for role in roles])


@app.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    role = storage.get(Roles, role_id)
    if not role:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(role.to_dict())


@app.route('/roles', methods=['POST'])
def create_role():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_role = Roles(**data)
    new_role.save()
    return make_response(jsonify(new_role.to_dict()), 201)


@app.route('/roles/<int:role_id>', methods=['PUT'])
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


@app.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    role = storage.get(Roles, role_id)
    if not role:
        return make_response(jsonify({'error': 'Not found'}), 404)
    role.delete()
    storage.save()
    return make_response(jsonify({}), 200)


# Reviews Routes
@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = storage.all(Reviews).values()
    return jsonify([review.to_dict() for review in reviews])


@app.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Reviews, review_id)
    if not review:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(review.to_dict())


@app.route('/reviews', methods=['POST'])
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


@app.route('/reviews/<review_id>', methods=['PUT'])
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


@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Reviews, review_id)
    if not review:
        return make_response(jsonify({'error': 'Not found'}), 404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('JOPMED_API_HOST')
    port = environ.get('JOPMED_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
