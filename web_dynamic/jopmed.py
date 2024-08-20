from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.route('/', strict_slashes=False)
@app.route('/jopmed-home', strict_slashes=False)
def jopmed():
    return render_template('index.html')

@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()
