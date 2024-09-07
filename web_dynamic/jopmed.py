import os
import requests
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify, request, abort
from flask_cors import CORS
from models import storage
from models.users import User
from models.shopping_cart import ShoppingCart
from models.products import Products
from models.service import Service
from datetime import timedelta
import requests
import models
import logging


app = Flask(__name__)
app.secret_key = 'jopmed_secret_key'
app.config['SESSION_COOKIE_SECURE'] = True  # for HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Set session to last for 7 days

cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# app_views = Blueprint('app_views', __name__, url_prefix='/api')

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
    if 'user_id' not in session:
        flash('Please log in to view your account', 'error')
        return redirect(url_for('login'))

    try:
        headers = {'User-ID': str(session['user_id'])}
        response = requests.get(f'{API_BASE_URL}/account', headers=headers, cookies=request.cookies, timeout=5)
        response.raise_for_status()
        user_data = response.json()
        return render_template('account.html', user=user_data)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch account details: {str(e)}")
        flash('Failed to fetch account details. Please try again.', 'error')
        return redirect(url_for('login'))



@app.route('/cart', methods=['GET'])
def cart_page():
    if 'user_id' not in session:
        flash('Please log in to view your cart.', 'error')
        return redirect(url_for('login'))

    try:
        response = requests.get(f'{API_BASE_URL}/cart', headers={'User-ID': session['user_id']}, timeout=5)
        response.raise_for_status()
        cart_items = response.json()
        return render_template('cart.html', cart_items=cart_items)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch cart items: {str(e)}")
        flash('Failed to fetch cart items. Please try again later.', 'error')
        return render_template('cart.html', cart_items=[])

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    user_id = session['user_id']
    product_id = data.get('product_id')
    service_id = data.get('service_id')
    quantity = data.get('quantity', 1)

    if not (product_id or service_id) or not quantity:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        response = requests.post(f'{API_BASE_URL}/cart/add', json={
            'user_id': user_id,
            'product_id': product_id,
            'service_id': service_id,
            'quantity': quantity
        }, timeout=5)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Failed to add to cart: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/cart/update', methods=['POST'])
def update_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    user_id = session['user_id']
    item_id = data.get('item_id')
    quantity = data.get('quantity')

    if not item_id or quantity is None:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        response = requests.post(f'{API_BASE_URL}/cart/update', json={
            'user_id': user_id,
            'item_id': item_id,
            'quantity': quantity
        }, timeout=5)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Failed to update cart: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/cart/remove', methods=['DELETE'])
def remove_from_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    user_id = session['user_id']
    item_id = data.get('item_id')

    if not item_id:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        response = requests.delete(f'{API_BASE_URL}/cart/remove', json={
            'user_id': user_id,
            'item_id': item_id
        }, timeout=5)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Failed to remove from cart: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        response = requests.post(f'{API_BASE_URL}/cart/clear', json={'user_id': session['user_id']}, timeout=5)
        if response.status_code == 200:
            return jsonify({'success': True}), 200
        else:
            error_message = response.json().get('error', 'Unknown error occurred')
            app.logger.error(f"Failed to clear cart: {error_message}")
            return jsonify({'error': error_message}), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Failed to clear cart: {str(e)}")
        return jsonify({'error': 'Failed to connect to the server'}), 500

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
        app.logger.debug(f"Products fetched: {products}")
        return render_template('products.html', products=products)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch products: {str(e)}")
        flash('Failed to fetch products. Please try again later.', 'error')
        return render_template('products.html', products=[])

@app.route('/api/products', methods=['GET'])
def get_products():
    products = storage.all(Products).values()
    return jsonify([product.to_dict(include_image=True) for product in products])

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
        flash('Failed to fetch reviews. Please try again later.', 'error')
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
        flash('Failed to fetch services. Please try again later.', 'error')
        return render_template('services.html', services=[])

@app.route('/shipping-information', strict_slashes=False)
def shipping_information():
    return render_template('shipping-information.html', shipping_info=[])

@app.route('/login', strict_slashes=False, methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/logout', strict_slashes=False, methods=['GET'])
def logout():
    # return render_template('logout.html')
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/register', strict_slashes=False, methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/checkout', methods=['GET'])
def checkout():
    if 'user_id' not in session:
        flash('Please log in to proceed to checkout.', 'error')
        return redirect(url_for('login'))

    try:
        headers = {'User-ID': str(session['user_id'])}
        response = requests.get(f'{API_BASE_URL}/cart', headers=headers, timeout=5)
        response.raise_for_status()
        cart_items = response.json()
        return render_template('checkout.html', cart_items=cart_items)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch cart items for checkout: {str(e)}")
        flash('Failed to fetch cart items. Please try again later.', 'error')
        return render_template('checkout.html', cart_items=[])



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

@app.route('/wishlist', methods=['GET'])
def view_wishlist():
    if 'user_id' not in session:
        flash('Please log in to view your wishlist', 'error')
        return redirect(url_for('login'))

    try:
        headers = {'User-ID': str(session['user_id'])}
        response = requests.get(f'{API_BASE_URL}/wishlist', headers=headers, timeout=5)
        response.raise_for_status()
        wishlist_items = response.json()
        return render_template('wishlist.html', wishlist_items=wishlist_items)
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch wishlist items: {str(e)}")
        flash('Failed to fetch wishlist items. Please try again.', 'error')
        return render_template('wishlist.html', wishlist_items=[])

@app.route('/wishlist/add', methods=['POST'])
def add_to_wishlist():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.form.to_dict()
    data['user_id'] = session['user_id']
    try:
        response = requests.post(f'{API_BASE_URL}/wishlist', json=data, timeout=5)
        response.raise_for_status()
        flash('Item added to wishlist successfully', 'success')
        return redirect(url_for('view_wishlist'))
    except requests.RequestException as e:
        app.logger.error(f"Failed to add item to wishlist: {str(e)}")
        flash('Failed to add item to wishlist. Please try again.', 'error')
        return redirect(url_for('view_wishlist'))

@app.route('/wishlist/update/<int:item_id>', methods=['POST'])
def update_wishlist_item(item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.form.to_dict()
    data['user_id'] = session['user_id']
    data['id'] = item_id
    try:
        response = requests.put(f'{API_BASE_URL}/wishlist', json=data, timeout=5)
        response.raise_for_status()
        flash('Wishlist item updated successfully', 'success')
        return redirect(url_for('view_wishlist'))
    except requests.RequestException as e:
        app.logger.error(f"Failed to update wishlist item: {str(e)}")
        flash('Failed to update wishlist item. Please try again.', 'error')
        return redirect(url_for('view_wishlist'))

@app.route('/wishlist/remove/<int:item_id>', methods=['POST'])
def remove_from_wishlist(item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = {'user_id': session['user_id'], 'id': item_id}
    try:
        response = requests.delete(f'{API_BASE_URL}/wishlist', json=data, timeout=5)
        response.raise_for_status()
        flash('Item removed from wishlist successfully', 'success')
        return redirect(url_for('view_wishlist'))
    except requests.RequestException as e:
        app.logger.error(f"Failed to remove item from wishlist: {str(e)}")
        flash('Failed to remove item from wishlist. Please try again.', 'error')
        return redirect(url_for('view_wishlist'))

if __name__ == "__main__":
    print("Running Flask application...")
    app.run(host='0.0.0.0', port=3000, debug=True)