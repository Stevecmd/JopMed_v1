from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SWAGGER'] = {
   'title': 'JOPMED Restful API',
   'uiversion': 3
}
Swagger(app)
