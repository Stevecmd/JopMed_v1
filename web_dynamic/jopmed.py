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

API_BASE_URL = 'http://localhost:5000/api'

print("Starting Flask application...")

@app.route('/', strict_slashes=False)
@app.route('/jopmed-home', strict_slashes=False)
def jopmed():
    """Render the home page"""
    return render_template('index.html')

@app.after_request
def clear_flashes(response):
    session.pop('_flashes', None)
    return response

@app.route('/about', strict_slashes=False)
def about():
    return render_template('about.html')

@app.route('/account', strict_slashes=False)
def account():
    try:
        response = requests.get(f'{API_BASE_URL}/account', timeout=5)
        response.raise_for_status()
        user = response.json()
        return render_template('account.html', user=user)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch account details: {str(e)}")
        flash(f'Failed to fetch account details: {str(e)}', 'error')
        return redirect(url_for('login'))



@app.route('/cart', methods=['GET'])
def cart_page():
    try:
        # Get the session ID
        user_id = session.get('user_id')
        if not user_id:
            flash('Please log in to view your cart', 'error')
            return redirect(url_for('login'))

        # Make a request to the API with the user ID in the headers
        headers = {'User-ID': str(user_id)}
        response = requests.get(f'{API_BASE_URL}/cart', headers=headers, timeout=5)
        response.raise_for_status()
        cart_items = response.json()
        return render_template('cart.html', cart_items=cart_items)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch cart items: {str(e)}")
        flash(f'Failed to fetch cart items: {str(e)}', 'error')
        return render_template('cart.html', cart_items=[])

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    data['user_id'] = session['user_id']
    try:
        response = requests.post(f'{API_BASE_URL}/cart/add', json=data, timeout=5)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Failed to add item to cart: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/cart/remove', methods=['DELETE'])
def remove_from_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    data['user_id'] = session['user_id']
    try:
        response = requests.delete(f'{API_BASE_URL}/cart/remove', json=data, timeout=5)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Failed to remove item from cart: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/cart/update_cart_item', methods=['POST'])
def update_cart_item():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    data['user_id'] = session['user_id']
    try:
        response = requests.post(f'{API_BASE_URL}/cart/update_cart_item', json=data, timeout=5)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Error updating cart: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/categories', strict_slashes=False)
def categories():
    try:
        response = requests.get(f'{API_BASE_URL}/categories', timeout=5)
        response.raise_for_status()
        categories = response.json()
        return render_template('categories.html', categories=categories)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch categories: {str(e)}")
        flash('Failed to fetch categories', 'error')
        return render_template('categories.html', categories=[])

@app.route('/contact-us', strict_slashes=False)
def contact_us():
    return render_template('contact-us.html')

@app.route('/orders', strict_slashes=False)
def orders():
    try:
        response = requests.get(f'{API_BASE_URL}/orders', timeout=5)
        response.raise_for_status()
        orders = response.json()
        return render_template('orders.html', orders=orders)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch orders: {str(e)}")
        flash('Failed to fetch orders', 'error')
        return render_template('orders.html', orders=[])

@app.route('/products', strict_slashes=False)
def products():
    try:
        response = requests.get(f'{API_BASE_URL}/products', timeout=5)
        response.raise_for_status()
        products = response.json()
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
    try:
        response = requests.get(f'{API_BASE_URL}/reviews', timeout=5)
        response.raise_for_status()
        reviews = response.json()
        return render_template('reviews.html', reviews=reviews)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch reviews: {str(e)}")
        flash('Failed to fetch reviews', 'error')
        return render_template('reviews.html', reviews=[])

@app.route('/services', strict_slashes=False)
def services():
    try:
        response = requests.get(f'{API_BASE_URL}/services', timeout=5)
        response.raise_for_status()
        services = response.json()
        return render_template('services.html', services=services)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch services: {str(e)}")
        flash('Failed to fetch services from the server. Showing local data.', 'warning')
        services = [
            {"id": 1, "name": "Service 1", "description": "Description 1"},
            {"id": 2, "name": "Service 2", "description": "Description 2"},
        ]
        return render_template('services.html', services=services)

@app.route('/shipping-information', strict_slashes=False)
def shipping_information():
    try:
        response = requests.get(f'{API_BASE_URL}/shipping_information', timeout=5)
        response.raise_for_status()
        shipping_info = response.json()
        return render_template('shipping-information.html', shipping_info=shipping_info)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch shipping information: {str(e)}")
        flash('Failed to fetch shipping information', 'error')
        return render_template('shipping-information.html', shipping_info=[])

@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        try:
            response = requests.post(f'{API_BASE_URL}/login', data=data, timeout=5)
            response.raise_for_status()
            flash('Login successful', 'success')
            return redirect(url_for('jopmed'))
        except requests.RequestException as e:
            app.logger.error(f"Failed to log in: {str(e)}")
            flash('Failed to log in. Please try again.', 'error')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout', strict_slashes=False, methods=['GET', 'POST'])
# @login_required
def logout():
    try:
        response = requests.post(f'{API_BASE_URL}/logout', timeout=5)
        response.raise_for_status()
        flash('Logged out successfully', 'success')
        if request.method == 'POST':
            return jsonify({'message': 'Logged out successfully'}), 200
        return redirect(url_for('login'))
    except requests.RequestException as e:
        app.logger.error(f"Failed to log out: {str(e)}")
        flash('Failed to log out. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        try:
            response = requests.post(f'{API_BASE_URL}/register', data=data, timeout=5)
            response.raise_for_status()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except requests.RequestException as e:
            app.logger.error(f"Failed to register: {str(e)}")
            flash('Failed to register. Please try again.', 'error')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/checkout', methods=['GET'])
def checkout():
    try:
        response = requests.get(f'{API_BASE_URL}/cart', timeout=5)
        response.raise_for_status()
        cart_items = response.json()
        
        if not cart_items:
            flash('Your cart is empty', 'error')
            return redirect(url_for('cart_page'))
        
        total_amount = sum(item['product']['price'] * item['quantity'] for item in cart_items if item.get('product'))
        return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch checkout data: {str(e)}")
        flash('Failed to load checkout. Please try again later.', 'error')
        return redirect(url_for('cart_page'))


@app.route('/register-payment-method', strict_slashes=False, methods=['GET', 'POST'])
def register_payment_method():
    if request.method == 'POST':
        data = {
            'user_id': session.get('user_id'),
            'payment_method': {
                'card_number': request.form.get('card_number'),
                'card_expiry': request.form.get('card_expiry'),
                'card_cvv': request.form.get('card_cvv'),
                'card_holder_name': request.form.get('card_holder_name')
            }
        }
        try:
            response = requests.post(f'{API_BASE_URL}/register-payment-method', json=data, timeout=5)
            response.raise_for_status()
            flash('Payment method registered successfully.', 'success')
            return redirect(url_for('account'))
        except requests.RequestException as e:
            app.logger.error(f"Failed to register payment method: {str(e)}")
            flash('Failed to register payment method. Please try again.', 'error')
            return render_template('register-payment-method.html')
    return render_template('register-payment-method.html')

if __name__ == "__main__":
    print("Running Flask application...")
    app.run(host='0.0.0.0', port=3000, debug=True)