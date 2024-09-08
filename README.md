# JopMed - The Console
The console is the first segment of the JopMed project.

#### Functionalities of this command interpreter:
* Create a new object (ex: a new User or a new Place)
* Retrieve an object from a file, a database etc...
* Do operations on objects (count, compute stats, etc...)
* Update attributes of an object
* Destroy an object

## Table of Contents


## Environment
This project is interpreted/tested on Ubuntu 14.04 LTS using python3 (version 3.4.3)

### Activate a Virtual environment:
- Create a Virtual Environment:
`python3 -m venv myvenv`

- Activate the Virtual Environment:
`source myvenv/bin/activate`

### Install requirements
`pip install -r requirements.txt`

## Installation
* Clone this repository: `git clone ""`
* Access Jopmed directory: `cd JOPMED_V1`
* Run jopmed(interactively): `./console.py` and enter command
* If it doesnt work use an explicit path for example: `python /media/stevecmd/48444E06444DF6EA/ALX/JopMed_v1/console.py`
* Run jopmed(non-interactively): `echo "<command>" | ./console.py`

## RESTful API
The project relies on a `RESTful - Flask API`. <br />
Below is a breakdown of the key aspects:
1. Flask Application: The code starts by importing necessary modules and creating a Flask application instance.
2. CORS Configuration: The CORS (Cross-Origin Resource Sharing) module is used to allow cross-origin requests to the API.
3. Error Handling: The code defines a custom 404 error handler to return a JSON response for not found resources.
4. Swagger Documentation: The Flasgger library is used to generate Swagger documentation for the API.
5. Routes and Endpoints: The API defines several routes and endpoints for managing users, addresses, orders, doctors, comments, and other entities. These endpoints support HTTP methods like GET, POST, PUT, and DELETE.
6. Database Storage: The code interacts with a storage engine (likely an ORM like SQLAlchemy) to perform CRUD (Create, Read, Update, Delete) operations on the database models.
7. Response Handling: The API returns JSON responses for successful operations and provides appropriate error responses for failed requests.

## File Descriptions


#### `models/` directory contains classes used for this project:
[base_model.py](/models/base_model.py) - The BaseModel class from which future classes will be derived
* `def __init__(self, *args, **kwargs)` - Initialization of the base model
* `def __str__(self)` - String representation of the BaseModel class
* `def save(self)` - Updates the attribute `updated_at` with the current datetime
* `def to_dict(self)` - Returns a dictionary containing all keys/values of the instance
* `def delete(self)` - Deletes the current instance from the storage

Classes inherited from Base Model:
* [addresses.py](/models/addresses.py)
* [categories.py](/models/categories.py)
* [comments.py](/models/comments.py)
* [doctors.py](/models/doctors.py)
* [file_uploads.py](/models/file_uploads.py)
* [inventory.py](/models/inventory.py)
* [order_items.py](/models/order_items.py)
* [orders.py](/models/orders.py)
* [payment_information.py](/models/payment_information.py)
* [payments.py](/models/payments.py)
* [prescriptions.py](/models/prescriptions.py)
* [product_categories.py](/models/product_categories.py)
* [product_images.py](/models/product_images.py)
* [product_tags.py](/models/product_tags.py)
* [products.py](/models/products.py)
* [reviews.py](/models/reviews.py)
* [roles.py](/models/roles.py)
* [shipping_information.py](/models/shipping_information.py)
* [shipping_methods.py](/models/shipping_methods.py)
* [tags.py](/models/tags.py)
* [user_roles.py](/models/user_roles.py)
* [users.py](/models/users.py)



## Examples of use
```
vagrant JOPMED_V1 $./console.py
(jopmed_v1) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  exit  show  update

(jopmed_v1) all MyModel
** class doesn't exist **
(jopmed_v1) create BaseModel
7da56403-cc45-4f1c-ad32-bfafeb2bb050
(jopmed_v1) all BaseModel
[[BaseModel] (7da56403-cc45-4f1c-ad32-bfafeb2bb050) {'updated_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772167), 'id': '7da56403-cc45-4f1c-ad32-bfafeb2bb050', 'created_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772123)}]
(jopmed_v1) show BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
[BaseModel] (7da56403-cc45-4f1c-ad32-bfafeb2bb050) {'updated_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772167), 'id': '7da56403-cc45-4f1c-ad32-bfafeb2bb050', 'created_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772123)}
(jopmed_v1) destroy BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
(jopmed_v1) show BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
** no instance found **
(jopmed_v1) quit
```

## Tools
[SQL-Checker](https://www.coderstool.com/sql-syntax-checker)

## Bugs
No known bugs at this time. 

## Authors
Patrick Odhiambo - [Github](https://github.com/patty6339) / [Twitter](https://twitter.com/patwafx) <br />
Steve Murimi - [Github](https://github.com/Stevecmd) / [Twitter](https://twitter.com/stevedevex)

## License
Public Domain. No copy write protection. 


User roles are used to manage and control access to different parts of an application or system. They help in defining what actions a user can perform based on their assigned role. Here are some common purposes of user roles:

`Access Control`: Restrict access to certain features or data based on the user's role. For example, an admin might have access to all parts of the system, while a regular user has limited access.
`Permission Management`: Define specific permissions for each role, such as read, write, update, and delete permissions for different resources.
`Security`: Enhance security by ensuring that only authorized users can perform certain actions, reducing the risk of unauthorized access.
`User Management`: Simplify user management by grouping users with similar permissions into roles, making it easier to assign and manage permissions.
`Audit and Compliance`: Maintain an audit trail of actions performed by users based on their roles, which is useful for compliance and monitoring purposes.
<br />
In the context of your SQL schema, the users_roles table is used to associate users with their respective roles, and the roles table defines the different roles available in the system. This setup allows you to manage user permissions and access control effectively.