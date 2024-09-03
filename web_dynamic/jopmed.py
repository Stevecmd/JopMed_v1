import os
import requests
from flask import Flask, render_template, session, redirect, url_for, flash
from models import storage

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
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    response = requests.get(f'{API_BASE_URL}/users/{user_id}')
    if response.status_code == 200:
        user = response.json()
        return render_template('account.html', user=user)
    else:
        flash('Failed to fetch account details', 'error')
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
        response = requests.post(f'{API_BASE_URL}/login', data=data)
        if response.status_code == 200:
            user = response.json()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully', 'success')
            session['show_popup'] = True
            return redirect(url_for('account'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/log-out', strict_slashes=False, methods=['POST'])
def log_out():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('log_in'))

@app.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        
        # Convert password to password_hash
        password = data.pop('password', None)
        if password:
            # You could hash the password here, or let the API do it as in the API route above
            data['password_hash'] = password
        
        response = requests.post(f'{API_BASE_URL}/users', json=data)
        if response.status_code == 201:
            flash('User registered successfully', 'success')
            return redirect(url_for('login'))
        else:
            flash('Failed to register user', 'error')
    
    return render_template('register.html')

@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    print("Running Flask application...")
    app.run(host='0.0.0.0', port=3000, debug=True)