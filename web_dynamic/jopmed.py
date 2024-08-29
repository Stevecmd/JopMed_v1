import os
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


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
    return render_template('account.html')

@app.route('/cart', strict_slashes=False)
def cart():
    return render_template('cart.html')

@app.route('/categories', strict_slashes=False)
def categories():
    return render_template('categories.html')

@app.route('/contact-us', strict_slashes=False)
def contact_us():
    return render_template('contact-us.html')

@app.route('/orders', strict_slashes=False)
def orders():
    return render_template('orders.html')

@app.route('/products', strict_slashes=False)
def products():
    return render_template('products.html')

@app.route('/admin', strict_slashes=False)
def admin():
    return render_template('admin.html')

@app.route('/reviews', strict_slashes=False)
def reviews():
    return render_template('reviews.html')

@app.route('/services', strict_slashes=False)
def services():
    return render_template('services.html')

@app.route('/shipping-information', strict_slashes=False)
def shipping_information():
    return render_template('shipping-information.html')

@app.route('/sign-in', strict_slashes=False)
def sign_in():
    return render_template('sign-in.html')

@app.route('/sign-out', strict_slashes=False)
def sign_out():
    return render_template('sign-out.html')

@app.route('/sign-up', strict_slashes=False)
def sign_up():
    return render_template('sign-up.html')


@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    print("Running Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
