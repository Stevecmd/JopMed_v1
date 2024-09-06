import os
import requests
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify, request, abort
from models import storage
from models.users import User
from werkzeug.security import check_password_hash, generate_password_hash
from models.shopping_cart import ShoppingCart
from models.products import Products
from models.service import Service
import models
import logging
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'jopmed_secret_key'
app.config['SESSION_COOKIE_SECURE'] = True  # for HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Set session to last for 7 days

API_BASE_URL = 'http://localhost:5000'

print("Starting Flask application...")

@app.route('/', strict_slashes=False)
@app.route('/jopmed-home', strict_slashes=False)
def jopmed():
    return render_template('index.html')

@app.route('/about', strict_slashes=False)
def about():
    return render_template('about.html')

@app.route('/account', strict_slashes=False)
def account():
    if 'user_id' not in session:
        flash('Please log in to view your account', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    try:
        response = requests.get(f'{API_BASE_URL}/users/{user_id}', timeout=5)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        user = response.json()
        return render_template('account.html', user=user)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch account details: {str(e)}")
        flash(f'Failed to fetch account details: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/cart', methods=['GET'])
def get_cart_api():
    """Retrieves the current user's cart"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    if models.storage_t == "db":
        cart_items = storage.session.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).all()
    else:
        all_cart_items = storage.all(ShoppingCart).values()
        cart_items = [item for item in all_cart_items if item.user_id == user_id]
    
    return jsonify([item.to_dict() for item in cart_items])

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Adds an item to the cart"""
    data = request.get_json()
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    item_id = data.get('item_id')
    item_type = data.get('item_type')  # 'product' or 'service'
    quantity = data.get('quantity', 1)

    if item_type == 'product':
        item = storage.get(Products, item_id)
    elif item_type == 'service':
        item = storage.get(Service, item_id)
    else:
        return jsonify({"error": "Invalid item type"}), 400

    if not item:
        return jsonify({"error": "Item not found"}), 404

    cart_item = ShoppingCart(user_id=user_id, quantity=quantity)
    if item_type == 'product':
        cart_item.product_id = item_id
    else:
        cart_item.service_id = item_id

    storage.new(cart_item)
    storage.save()

    return jsonify({"success": True, "message": "Item added to cart"}), 200

@app.route('/cart/remove', methods=['DELETE'])
def remove_from_cart():
    """Removes an item from the cart"""
    data = request.get_json()
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    item_id = data.get('item_id')

    if models.storage_t == "db":
        cart_item = storage.session.query(ShoppingCart).filter(
            ShoppingCart.user_id == user_id,
            (ShoppingCart.product_id == item_id) | (ShoppingCart.service_id == item_id)
        ).first()
    else:
        all_cart_items = storage.all(ShoppingCart).values()
        cart_item = next((item for item in all_cart_items if item.user_id == user_id and (item.product_id == item_id or item.service_id == item_id)), None)

    if not cart_item:
        return jsonify({"error": "Item not found in cart"}), 404

    storage.delete(cart_item)
    storage.save()

    return jsonify({"success": True, "message": "Item removed from cart"}), 200

@app.route('/cart/update_cart_item', methods=['POST'])
def update_cart_item():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        
        data = request.get_json()
        user_id = session['user_id']
        item_id = data.get('item_id')
        quantity_change = data.get('quantity')
        
        if not item_id or quantity_change is None:
            return jsonify({"error": "Invalid data"}), 400
        
        cart_items = storage.all(ShoppingCart)
        cart_item = next((item for item in cart_items.values() if item.user_id == user_id and item.product_id == item_id), None)
        
        if not cart_item:
            cart_item = ShoppingCart(user_id=user_id, product_id=item_id, quantity=quantity_change)
            storage.new(cart_item)
        else:
            cart_item.quantity += quantity_change
            if cart_item.quantity <= 0:
                storage.delete(cart_item)
            
        storage.save()
        
        return jsonify({"success": True, "message": "Cart updated successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error updating cart: {str(e)}")
        return jsonify({"error": "An error occurred while updating the cart"}), 500


@app.route('/categories', strict_slashes=False)
def categories():
    response = requests.get(f'{API_BASE_URL}/categories')
    if response.status_code == 200:
        categories = response.json()
        return render_template('categories.html', categories=categories)
    else:
        flash('Failed to fetch categories', 'error')
        return render_template('categories.html', categories=[])

@app.route('/contact-us', strict_slashes=False)
def contact_us():
    return render_template('contact-us.html')

@app.route('/orders', strict_slashes=False)
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    response = requests.get(f'{API_BASE_URL}/orders')
    if response.status_code == 200:
        orders = response.json()
        return render_template('orders.html', orders=orders)
    else:
        flash('Failed to fetch orders', 'error')
        return render_template('orders.html', orders=[])

@app.route('/products', strict_slashes=False)
def products():
    try:
        response = requests.get(f'{API_BASE_URL}/products', timeout=5)
        response.raise_for_status()
        products = response.json()  # Ensure to parse JSON, not text
        return render_template('products.html', products=products)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch products: {str(e)}")
        flash('Failed to fetch products. Please try again later.', 'error')
        return render_template('products.html', products=[])

@app.route('/admin', strict_slashes=False)
def admin():
    return render_template('admin.html')

@app.route('/reviews', strict_slashes=False)
def reviews():
    response = requests.get(f'{API_BASE_URL}/reviews')
    if response.status_code == 200:
        reviews = response.json()
        return render_template('reviews.html', reviews=reviews)
    else:
        flash('Failed to fetch reviews', 'error')
        return render_template('reviews.html', reviews=[])

@app.route('/services', strict_slashes=False)
def services():
    try:
        response = requests.get(f'{API_BASE_URL}/services', timeout=5)
        response.raise_for_status()
        services = response.json()
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch services: {str(e)}")
        flash('Failed to fetch services from the server. Showing local data.', 'warning')
        # Provide some default or cached services data
        services = [
            {"id": 1, "name": "Service 1", "description": "Description 1"},
            {"id": 2, "name": "Service 2", "description": "Description 2"},
            # Add more default services as needed
        ]
    
    return render_template('services.html', services=services)

@app.route('/shipping-information', strict_slashes=False)
def shipping_information():
    response = requests.get(f'{API_BASE_URL}/shipping_information')
    if response.status_code == 200:
        shipping_info = response.json()
        return render_template('shipping-information.html', shipping_info=shipping_info)
    else:
        flash('Failed to fetch shipping information', 'error')
        return render_template('shipping-information.html', shipping_info=[])

from flask import request

@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        logging.debug(f"Login data: {data}")
        
        if not data or 'username' not in data or 'password' not in data:
            flash('Invalid data', 'error')
            return redirect(url_for('login'))
        
        users = storage.filter(User, username=data['username'])
        user = users[0] if users else None
        
        if user and check_password_hash(user.password_hash, data['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True  # Make the session persistent
            flash('Logged in successfully', 'success')
            return redirect(url_for('jopmed'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout', strict_slashes=False, methods=['POST'])
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        
        # Check if username already exists
        if storage.filter(User, username=data['username']):
            flash('Username already exists', 'error')
            return redirect(url_for('register'))

        # Check if email already exists
        if storage.filter(User, email=data['email']):
            flash('Email already exists', 'error')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        new_user.set_password(data['password'])
        
        try:
            storage.new(new_user)
            storage.save()
            flash('User registered successfully', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'An error occurred during registration: {str(e)}', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()

@app.route('/cart', methods=['GET'])
def cart_page():
    return render_template('cart.html')

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Retrieves the current user's cart"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    if models.storage_t == "db":
        cart_items = storage.session.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).all()
    else:
        all_cart_items = storage.all(ShoppingCart).values()
        cart_items = [item for item in all_cart_items if item.user_id == user_id]
    
    return jsonify([item.to_dict() for item in cart_items])

@app.route('/check_login', methods=['GET'])
def check_login():
    logged_in = 'user_id' in session and 'username' in session
    user_id = session.get('user_id')
    username = session.get('username')
    print(f"Session contents: {session}")
    print(f"User logged in: {logged_in}, User ID: {user_id}, Username: {username}")
    return jsonify({'logged_in': logged_in, 'user_id': user_id, 'username': username})

@app.route('/api/protected_route', methods=['GET'])
def protected_route():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session['user_id']
    
    # Fetch user-specific data from your API
    try:
        # Get user details
        user_response = requests.get(f'{API_BASE_URL}/users/{user_id}', timeout=5)
        user_response.raise_for_status()
        user_data = user_response.json()

        # Get user's orders
        orders_response = requests.get(f'{API_BASE_URL}/users/{user_id}/orders', timeout=5)
        orders_response.raise_for_status()
        orders_data = orders_response.json()

        # Get user's reviews
        reviews_response = requests.get(f'{API_BASE_URL}/users/{user_id}/reviews', timeout=5)
        reviews_response.raise_for_status()
        reviews_data = reviews_response.json()

        # Combine all the data
        protected_data = {
            'user': user_data,
            'orders': orders_data,
            'reviews': reviews_data
        }

        return jsonify(protected_data), 200

    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch protected data: {str(e)}")
        return jsonify({'error': 'Failed to fetch protected data'}), 500

@app.before_request
def before_request():
    print(f"Session before request: {session}")

@app.route('/user/ratings', methods=['GET'])
def get_user_ratings():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    
    user_id = session['user_id']
    try:
        response = requests.get(f'{API_BASE_URL}/user/ratings', cookies=request.cookies)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Error fetching user ratings: {str(e)}")
        return jsonify({'error': 'Failed to fetch user ratings'}), 500

@app.route('/checkout', methods=['GET'])
def checkout():
    if 'user_id' not in session:
        flash('Please log in to proceed to checkout', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    try:
        response = requests.get(f'{API_BASE_URL}/checkout', cookies=request.cookies)
        response.raise_for_status()
        checkout_data = response.json()
        return render_template('checkout.html', checkout_data=checkout_data)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch checkout data: {str(e)}")
        flash('Failed to load checkout. Please try again later.', 'error')
        return redirect(url_for('cart_page'))

if __name__ == "__main__":
    print("Running Flask application...")
    app.run(host='0.0.0.0', port=3000, debug=True)