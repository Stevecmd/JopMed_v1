import os
import requests
from flask import Flask, render_template, session, redirect, url_for, flash
from models import storage
from models.users import User
from werkzeug.security import check_password_hash, generate_password_hash
import logging

app = Flask(__name__)
app.secret_key = 'jopmed_secret_key'

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

@app.route('/cart', strict_slashes=False)
def cart():
    return render_template('cart.html')

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
    response = requests.get(f'{API_BASE_URL}/products')
    if response.status_code == 200:
        products = response.json()
        return render_template('products.html', products=products)
    else:
        flash('Failed to fetch products', 'error')
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
    response = requests.get(f'{API_BASE_URL}/services')
    if response.status_code == 200:
        services = response.json()
        return render_template('services.html', services=services)
    else:
        flash('Failed to fetch services', 'error')
        return render_template('services.html', services=[])

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
            flash('Logged in successfully', 'success')
            return redirect(url_for('account'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout', strict_slashes=False, methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
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

if __name__ == "__main__":
    print("Running Flask application...")
    app.run(host='0.0.0.0', port=3000, debug=True)