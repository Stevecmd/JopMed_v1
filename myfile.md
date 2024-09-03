# Run the application
Starting a python env named myvenv:
```sh
python3 -m venv myvenv
source myvenv/bin/activate
deactivate
```
Install the required packages:
```sh
pip install -r requirements.txt
```
### Errors:
In the event of an error `Import "pycodestyle" could not be resolved`
Select the Python Interpreter: Make sure that Visual Studio Code is using the correct Python interpreter from your virtual environment. Do this by:

- Opening the Command Palette (`Ctrl+Shift+P`).
- Typing `Python: Select Interpreter`.
- Selecting the interpreter from your virtual environment (it should be something like `myvenv/bin/python`).

# MySQL
To set an empty password for the MySQL root user, follow these steps:
Log in to MySQL as the root user using sudo:
`sudo mysql -u root`

Switch to the mysql database:
`USE mysql;`

Update the authentication method for the root user to use the mysql_native_password plugin and set an empty password:
`ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';`

Flush the privileges to ensure that the changes take effect:
`FLUSH PRIVILEGES;`

Exit the MySQL shell:
`EXIT;`

0x04
- Dump data into MySQL database

Run the cat command again with the updated root user credentials:

`cat jopmed-dump-prod.sql| mysql -u root -p`

`cat jopmed-dump-prod.sql | mysql -u root --password=""`



- JOPMED is alive!
`cat jopmed-dump-prod.sql | mysql -uroot -p`

- Run the app
`JOPMED_MYSQL_USER=jopmed_dev JOPMED_MYSQL_PWD=jopmed_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=jopmed_dev_db JOPMED_TYPE_STORAGE=db python3 -m web_dynamic.jopmed`

- Run the API
`JOPMED_MYSQL_USER=jopmed_dev JOPMED_MYSQL_PWD=jopmed_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=jopmed_dev_db JOPMED_TYPE_STORAGE=db JOPMED_API_HOST=0.0.0.0 JOPMED_API_PORT=5000 python3 -m api.v1.app`

Running both the app and API have been simplified, run them by running: `./start_services.sh`
Ports: - `Frontend: 3000`
       - `API: 5000`

0x05
- Never Fail
`python3 -m unittest discover tests 2>&1 | tail -1`
Test the `Test` database and see the output:
1. `JOPMED_ENV=test JOPMED_MYSQL_USER=JOPMED_test JOPMED_MYSQL_PWD=JOPMED_test_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_test_db JOPMED_TYPE_STORAGE=db python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1`
2. Test using the test database:
`JOPMED_ENV=test JOPMED_MYSQL_USER=JOPMED_test JOPMED_MYSQL_PWD=JOPMED_test_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=jopmed_test_db JOPMED_TYPE_STORAGE=db python3 -m unittest discover tests`
3. Test .get() and .count() methods
`python3 ./test_get_count.py`

- Improve storage
`JOPMED_MYSQL_USER=JOPMED_dev JOPMED_MYSQL_PWD=JOPMED_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_dev_db JOPMED_TYPE_STORAGE=db ./test_get_count.py`

- Status of your API
`JOPMED_MYSQL_USER=jopmed_dev JOPMED_MYSQL_PWD=jopmed_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=jopmed_dev_db JOPMED_TYPE_STORAGE=db JOPMED_API_HOST=0.0.0.0 JOPMED_API_PORT=5000 python3 -m api.v1.app`

`curl -X GET http://0.0.0.0:5000/api/v1/status`

- Some users?
`curl -X GET http://0.0.0.0:5000/users`
Output:
```sh

[
  {
    "__class__": "User",
    "created_at": "2024-08-26T12:35:55.000000",
    "email": "johndoe@example.com",
    "first_name": "John",
    "id": 1,
    "last_name": "Doe",
    "updated_at": "2024-08-26T12:35:55.000000",
    "username": "johndoe"
  },
  {
    "__class__": "User",
    "created_at": "2024-08-26T12:35:55.000000",
    "email": "janedoe@example.com",
    "first_name": "Jane",
    "id": 2,
    "last_name": "Doe",
    "updated_at": "2024-08-26T12:35:55.000000",
    "username": "janedoe"
  },
  {
    "__class__": "User",
    "created_at": "2024-08-26T12:46:09.000000",
    "email": "newuser@example.com",
    "first_name": "Alice",
    "id": 3,
    "last_name": "Smith",
    "updated_at": "2024-08-26T12:46:09.000000",
    "username": "newuser"
  }
]

```
Insert a user into the database:
`curl -X POST http://0.0.0.0:5000/users -H "Content-Type: application/json" -d '{"username": "newuser", "email": "newuser@example.com", "password": "123456", "first_name": "Alice", "last_name": "Smith"}'`
Output:
```sh
{
  "__class__": "User",
  "created_at": "2024-08-26T12:46:09.237687",
  "email": "newuser@example.com",
  "first_name": "Alice",
  "id": 3,
  "last_name": "Smith",
  "updated_at": "2024-08-26T12:46:09.237710",
  "username": "newuser"
}
```
Retrieve a user with their id from the database:
```sh

curl -X GET http://0.0.0.0:5000/users/3
{
  "__class__": "User",
  "created_at": "2024-08-26T12:46:09.000000",
  "email": "newuser@example.com",
  "first_name": "Alice",
  "id": 3,
  "last_name": "Smith",
  "updated_at": "2024-08-26T12:46:09.000000",
  "username": "newuser"
}

```
Post a user to the database:
```sh

curl -X POST http://0.0.0.0:5000/users -H "Content-Type: application/json" -d '{"username": "Derrick", "em
ail": "derrick@example.com", "password": "123456", "first_name": "Derrick", "last_name": "Otongolo"}'

```
output:
```sh

{
  "__class__": "User",
  "created_at": "2024-08-26T13:02:38.960801",
  "email": "derrick@example.com",
  "first_name": "Derrick",
  "id": 4,
  "last_name": "Otongolo",
  "updated_at": "2024-08-26T13:02:38.960835",
  "username": "Derrick"
}

```
Delete a user:
```sh
curl -X DELETE http://127.0.0.1:5000/users/3
```
```sh
{
  "__class__": "User",
  "created_at": "2024-08-26T12:46:09.000000",
  "email": "newuser@example.com",
  "first_name": "Alice",
  "id": 3,
  "last_name": "Smith",
  "updated_at": "2024-08-26T12:46:09.000000",
  "username": "newuser"
}

```

Get Addresses:
```sh
curl -X GET http://127.0.0.1:5000/addresses
[
  {
    "__class__": "Addresses",
    "city": "New York",
    "country": "USA",
    "created_at": "2024-08-26T12:35:56.000000",
    "id": 1,
    "phone_number": "123-456-7890",
    "street_address": "123 Main St",
    "updated_at": "2024-08-26T12:35:56.000000",
    "user_id": 1,
    "zip_code": "10001"
  },
  {
    "__class__": "Addresses",
    "city": "Los Angeles",
    "country": "USA",
    "created_at": "2024-08-26T12:35:56.000000",
    "id": 2,
    "phone_number": "098-765-4321",
    "street_address": "456 Elm St",
    "updated_at": "2024-08-26T12:35:56.000000",
    "user_id": 2,
    "zip_code": "90001"
  }
]

```
Get Address by ID:
```sh
curl -X GET http://127.0.0.1:5000/addresses/1
{
  "__class__": "Addresses",
  "city": "New York",
  "country": "USA",
  "created_at": "2024-08-26T12:35:56.000000",
  "id": 1,
  "phone_number": "123-456-7890",
  "street_address": "123 Main St",
  "updated_at": "2024-08-26T12:35:56.000000",
  "user_id": 1,
  "zip_code": "10001"
}

```
Put an address:
```sh

curl -X PUT http://localhost:5000/addresses/1 -H "Content-Type: application/json" -d '{
  "user_id": 2,
  "city": "San Francisco",
  "country": "USA",
  "zip_code": "94101",
  "street_address": "789 Pine St",
  "phone_number": "321-654-0987"
}'
{
  "__class__": "Addresses",
  "city": "San Francisco",
  "country": "USA",
  "created_at": "2024-08-26T12:35:56.000000",
  "id": 1,
  "phone_number": "321-654-0987",
  "street_address": "789 Pine St",
  "updated_at": "2024-08-26T13:21:29.305898",
  "user_id": 2,
  "zip_code": "94101"
}

```
Delete an address:
```sh

curl -X DELETE http://localhost:5000/addresses/2
{
  "__class__": "Addresses",
  "city": "Los Angeles",
  "country": "USA",
  "created_at": "2024-08-26T12:35:56.000000",
  "id": 2,
  "phone_number": "098-765-4321",
  "street_address": "456 Elm St",
  "updated_at": "2024-08-26T12:35:56.000000",
  "user_id": 2,
  "zip_code": "90001"
}

```
Fetch orders:
```sh

curl -X GET http://127.0.0.1:5000/orders
[
  {
    "__class__": "Orders",
    "address_id": 0,
    "created_at": "2024-08-26T12:36:06.000000",
    "id": 1,
    "payment_method": "credit_card",
    "status": "pending",
    "total_amount": "15.99",
    "updated_at": "2024-08-26T12:36:06.000000",
    "user_id": 1
  },
  {
    "__class__": "Orders",
    "address_id": 0,
    "created_at": "2024-08-26T12:36:06.000000",
    "id": 2,
    "payment_method": "paypal",
    "status": "",
    "total_amount": "21.00",
    "updated_at": "2024-08-26T12:36:06.000000",
    "user_id": 2
  }
]

```
Fetch order using order id:
```sh

curl -X GET http://127.0.0.1:5000/orders/1
{
  "__class__": "Orders",
  "address_id": 0,
  "created_at": "2024-08-26T12:36:06.000000",
  "id": 1,
  "payment_method": "credit_card",
  "status": "pending",
  "total_amount": "15.99",
  "updated_at": "2024-08-26T12:36:06.000000",
  "user_id": 1
}

```
Posting orders:
```sh

curl -X POST http://127.0.0.1:5000/orders -H "Content-Type: application/json" -d '{
  "user_id": 2,
  "address_id": 1,
  "status": "pending",
  "payment_method": "credit_card",
  "total_amount": "30.50"
}'
{
  "__class__": "Orders",
  "address_id": 1,
  "created_at": "2024-08-26T13:55:36.613265",
  "id": 5,
  "payment_method": "credit_card",
  "status": "pending",
  "total_amount": "30.50",
  "updated_at": "2024-08-26T13:55:36.613279",
  "user_id": 2
}

```

Updating an order:
```sh

curl -X PUT http://localhost:5000/orders/5 -H "Content-Type: application/json" -d '{
  "status": "shipped",
  "total_amount": 35.00
}'
{
  "__class__": "Orders",
  "address_id": 1,
  "created_at": "2024-08-26T13:55:37.000000",
  "id": 5,
  "payment_method": "credit_card",
  "status": "shipped",
  "total_amount": 35.0,
  "updated_at": "2024-08-26T14:00:10.570694",
  "user_id": 2
}

```

Updating order_items:

```sh
curl -X POST http://localhost:5000/order_items -H "Content-Type: application/json" -d '{
  "order_id": 1,
  "product_id": 2,
  "quantity": 3,
  "price": 9.99
}'
{
  "__class__": "Order_Items",
  "created_at": "2024-08-26T14:30:29.163693",
  "id": 3,
  "order_id": 1,
  "price": 9.99,
  "product_id": 2,
  "quantity": 3,
  "updated_at": "2024-08-26T14:30:29.163712"
}

```

Get a list of doctors:
```sh

curl -X GET http://127.0.0.1:5000/doctors
[
  {
    "__class__": "Doctors",
    "created_at": "2024-08-26T12:36:20.000000",
    "first_name": "John",
    "id": 1,
    "last_name": "Smith",
    "phone_number": "123-456-7890",
    "specialization": "Cardiology",
    "updated_at": "2024-08-26T12:36:20.000000"
  },
  {
    "__class__": "Doctors",
    "created_at": "2024-08-26T12:36:20.000000",
    "first_name": "Jane",
    "id": 2,
    "last_name": "Doe",
    "phone_number": "098-765-4321",
    "specialization": "Neurology",
    "updated_at": "2024-08-26T12:36:20.000000"
  }
]

```
Get doctors by ID:
```sh

curl -X GET http://127.0.0.1:5000/doctors/1
{
  "__class__": "Doctors",
  "created_at": "2024-08-26T12:36:20.000000",
  "first_name": "John",
  "id": 1,
  "last_name": "Smith",
  "phone_number": "123-456-7890",
  "specialization": "Cardiology",
  "updated_at": "2024-08-26T12:36:20.000000"
}

```
Add a new doctor:
```sh

curl -X POST http://127.0.0.1:5000/doctors -H "Content-Type: application/json" -d '{
  "first_name": "Jane",
  "last_name": "Doe",
  "specialization": "Neurology",
  "phone_number": "987-654-3210",
  "email": "jane.doe1@example.com",
  "created_at": "2024-08-26T12:36:20.000000",
  "updated_at": "2024-08-26T12:36:20.000000"
}'
{
  "__class__": "Doctors",
  "created_at": "2024-08-26T12:36:20.000000",
  "email": "jane.doe1@example.com",
  "first_name": "Jane",
  "id": 5,
  "last_name": "Doe",
  "phone_number": "987-654-3210",
  "specialization": "Neurology",
  "updated_at": "2024-08-27T04:45:52.298382"
}

```
Adding doctors must use unique email:
```sh

curl -X POST http://127.0.0.1:5000/doctors -H "Content-Type: application/json" -d '{
  "first_name": "Jane",
  "last_name": "Doe",
  "specialization": "Neurology",
  "phone_number": "987-654-3210",
  "email": "jane.doe1@example.com",
  "created_at": "2024-08-26T12:36:20.000000",
  "updated_at": "2024-08-26T12:36:20.000000"
}'
{
  "error": "Email already exists"
}

```

Updating a doctor via ID:
```sh

curl -X PUT http://127.0.0.1:5000/doctors/1 \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Jonathan",
  "specialization": "Neurology"
}'
{
  "__class__": "Doctors",
  "created_at": "2024-08-26T12:36:20.000000",
  "email": "john.smith@example.com",
  "first_name": "Jonathan",
  "id": 1,
  "last_name": "Smith",
  "phone_number": "123-456-7890",
  "specialization": "Neurology",
  "updated_at": "2024-08-27T04:54:04.052726"
}

```
Delete a doctor via the ID:
```sh

curl -X DELETE http://127.0.0.1:5000/doctors/5

```

Get comments:
```sh

curl -X GET http://127.0.0.1:5000/comments
[
  {
    "__class__": "Comments",
    "content": "Great product, very effective!",
    "created_at": "2024-08-26T12:36:17.000000",
    "id": 1,
    "product_id": 1,
    "updated_at": "2024-08-26T12:36:17.000000",
    "user_id": 1
  },
  {
    "__class__": "Comments",
    "content": "Not satisfied with the quality.",
    "created_at": "2024-08-26T12:36:17.000000",
    "id": 2,
    "product_id": 2,
    "updated_at": "2024-08-26T12:36:17.000000",
    "user_id": 2
  }
]

```
Get comments by ID:
```sh

curl -X GET http://127.0.0.1:5000/comments/1
{
  "__class__": "Comments",
  "content": "Great product, very effective!",
  "created_at": "2024-08-26T12:36:17.000000",
  "id": 1,
  "product_id": 1,
  "updated_at": "2024-08-26T12:36:17.000000",
  "user_id": 1
}

```
Update a comment via ID:
```sh

curl -X PUT http://127.0.0.1:5000/comments/2 -H "Content-Type: application/json" -d '{"content": "Updated comment content"}'
{
  "__class__": "Comments",
  "content": "Updated comment content",
  "created_at": "2024-08-26T12:36:17.000000",
  "id": 2,
  "product_id": 2,
  "updated_at": "2024-08-27T05:08:56.137970",
  "user_id": 2
}

```
Delete a comment using its ID:
```sh
curl -X DELETE http://127.0.0.1:5000/comments/2
```

Get categories:
```sh

curl -X GET http://127.0.0.1:5000/categories
[
  {
    "__class__": "Categories",
    "created_at": "2024-08-26T12:36:01.000000",
    "description": "Various types of medicines",
    "id": 1,
    "name": "Medicines",
    "slug": "medicines",
    "updated_at": "2024-08-26T12:36:01.000000"
  },
  {
    "__class__": "Categories",
    "created_at": "2024-08-26T12:36:01.000000",
    "description": "Health supplements and vitamins",
    "id": 2,
    "name": "Supplements",
    "slug": "supplements",
    "updated_at": "2024-08-26T12:36:01.000000"
  }
]

```

Get categories by ID:
```sh
curl -X GET http://127.0.0.1:5000/categories/1
{
  "__class__": "Categories",
  "created_at": "2024-08-26T12:36:01.000000",
  "description": "Various types of medicines",
  "id": 1,
  "name": "Medicines",
  "slug": "medicines",
  "updated_at": "2024-08-26T12:36:01.000000"
}

```
Add a new category:
```sh

curl -X POST http://127.0.0.1:5000/categories -H "Content-Type: application/json" -d '{"name": "Disinfectants", "de
scription": "Disinfectants info", "slug": "disinfectants"}'
{
  "__class__": "Categories",
  "created_at": "2024-08-27T05:17:16.655630",
  "description": "Disinfectants info",
  "id": 3,
  "name": "Disinfectants",
  "slug": "disinfectants",
  "updated_at": "2024-08-27T05:17:16.655647"
}

```
Update a category by ID:
```sh

curl -X PUT h
ttp://127.0.0.1:5000/categories/3 -H "Content-Type: application/json" -d '{"name": "New-Disinfectants"
, "description": "New-Disinfectants info"}'
{
  "__class__": "Categories",
  "created_at": "2024-08-27T05:17:17.000000",
  "description": "New-Disinfectants info",
  "id": 3,
  "name": "New-Disinfectants",
  "slug": "disinfectants",
  "updated_at": "2024-08-27T05:19:33.280803"
}

```

Delete a category by ID:
```sh

curl -X DELETE http://127.0.0.1:5000/categories/3
{
  "success": "Category deleted"
}

```

Get all product categories:
```sh

curl -X GET h
ttp://127.0.0.1:5000/product_categories
[
  {
    "__class__": "Product_Categories",
    "category_id": 1,
    "created_at": "2024-08-26T12:36:02.000000",
    "id": 1,
    "product_id": 1,
    "updated_at": "2024-08-26T12:36:02.000000"
  },
  {
    "__class__": "Product_Categories",
    "category_id": 2,
    "created_at": "2024-08-26T12:36:02.000000",
    "id": 2,
    "product_id": 2,
    "updated_at": "2024-08-26T12:36:02.000000"
  }
]

```

Get product categories by ID:
```sh

curl -X GET http://127.0.0.1:5000/product_categories/1
[
  {
    "__class__": "Product_Categories",
    "category_id": 1,
    "created_at": "2024-08-26T12:36:02.000000",
    "id": 1,
    "product_id": 1,
    "updated_at": "2024-08-26T12:36:02.000000"
  }
]

```
Get product_categories via ID:
```sh

curl -X POST http://127.0.0.1:5000/product_categories      -H "Content-Type: application/json"      -d '{
           "product_id": 2,
           "category_id": 2
         }'
{
  "__class__": "Product_Categories",
  "category_id": 2,
  "created_at": "2024-08-27T05:45:26.592499",
  "id": 5,
  "product_id": 2,
  "updated_at": "2024-08-27T05:45:26.592513"
}

```

Get a list of prescriptions:
```sh

curl -X GET http://127.0.0.1:5000/prescriptions
[
  {
    "__class__": "Prescriptions",
    "created_at": "2024-08-27T09:40:44.000000",
    "doctor_id": 1,
    "dosage": "Dosage A",
    "expiration_date": "Wed, 27 Aug 2025 06:40:44 GMT",
    "id": 1,
    "instructions": "Instructions A",
    "medication": "Medication A",
    "prescription_date": "Tue, 27 Aug 2024 06:40:44 GMT",
    "updated_at": "2024-08-27T09:40:44.000000",
    "user_id": 1
  },
  {
    "__class__": "Prescriptions",
    "created_at": "2024-08-27T09:40:44.000000",
    "doctor_id": 2,
    "dosage": "Dosage B",
    "expiration_date": "Wed, 27 Aug 2025 06:40:44 GMT",
    "id": 2,
    "instructions": "Instructions B",
    "medication": "Medication B",
    "prescription_date": "Tue, 27 Aug 2024 06:40:44 GMT",
    "updated_at": "2024-08-27T09:40:44.000000",
    "user_id": 2
  }
]

```
Get a prescription by ID:
```sh

curl -X GET http://127.0.0.1:5000/prescriptions/1
{
  "__class__": "Prescriptions",
  "created_at": "2024-08-27T09:40:44.000000",
  "doctor_id": 1,
  "dosage": "Dosage A",
  "expiration_date": "Wed, 27 Aug 2025 06:40:44 GMT",
  "id": 1,
  "instructions": "Instructions A",
  "medication": "Medication A",
  "prescription_date": "Tue, 27 Aug 2024 06:40:44 GMT",
  "updated_at": "2024-08-27T09:40:44.000000",
  "user_id": 1
}

```
Get products images:
```sh

curl -X GET http://127.0.0.1:5000/product_images
[
  {
    "__class__": "Product_Images",
    "created_at": "2024-08-27T06:40:21.000000",
    "id": 1,
    "image_url": "http://example.com/images/paracetamol.jpg",
    "product_id": 1,
    "updated_at": "2024-08-27T06:40:21.000000"
  },
  {
    "__class__": "Product_Images",
    "created_at": "2024-08-27T06:40:21.000000",
    "id": 2,
    "image_url": "http://example.com/images/vitamin-c.jpg",
    "product_id": 2,
    "updated_at": "2024-08-27T06:40:21.000000"
  }
]

```
Get product images by ID:
```sh

curl -X GET http://127.0.0.1:5000/product_images/1
[
  {
    "__class__": "Product_Images",
    "created_at": "2024-08-27T06:40:21.000000",
    "id": 1,
    "image_url": "http://example.com/images/paracetamol.jpg",
    "product_id": 1,
    "updated_at": "2024-08-27T06:40:21.000000"
  }
]

```

Get Shipping methods:
```sh

curl -X GET http://127.0.0.1:5000/shipping_methods
[
  {
    "__class__": "Shipping_Methods",
    "created_at": "2024-08-27T06:40:13.000000",
    "description": "Delivery within 5-7 business days",
    "id": 1,
    "name": "Standard Shipping",
    "updated_at": "2024-08-27T06:40:13.000000"
  },
  {
    "__class__": "Shipping_Methods",
    "created_at": "2024-08-27T06:40:13.000000",
    "description": "Delivery within 1-2 business days",
    "id": 2,
    "name": "Express Shipping",
    "updated_at": "2024-08-27T06:40:13.000000"
  }
]

```
Get shipping methods by ID:
```sh

curl -X GET http://127.0.0.1:5000/shipping_methods/1
{
  "__class__": "Shipping_Methods",
  "created_at": "2024-08-27T06:40:13.000000",
  "description": "Delivery within 5-7 business days",
  "id": 1,
  "name": "Standard Shipping",
  "updated_at": "2024-08-27T06:40:13.000000"
}

```


- Not found
`curl -X GET http://0.0.0.0:5000/api/v1/nop`
`curl -X GET http://0.0.0.0:5000/api/v1/nop -vvv`


0x06
- Cash only
`JOPMED_MYSQL_USER=JOPMED_dev JOPMED_MYSQL_PWD=JOPMED_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_dev_db JOPMED_TYPE_STORAGE=db python3 -m web_dynamic.0-JOPMED`

- API status
`JOPMED_MYSQL_USER=JOPMED_dev JOPMED_MYSQL_PWD=JOPMED_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_dev_db JOPMED_TYPE_STORAGE=db JOPMED_API_PORT=5001 python3 -m api.v1.app`

Automatically update the `requirements.txt` file:
`pip freeze > requirements.txt`
