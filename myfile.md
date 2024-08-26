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
`JOPMED_MYSQL_USER=JOPMED_dev JOPMED_MYSQL_PWD=JOPMED_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_dev_db JOPMED_TYPE_STORAGE=db python3 -m web_dynamic.jopmed`

0x05
- Never Fail
`python3 -m unittest discover tests 2>&1 | tail -1`
Test the `Test` database and see the output:
1. `JOPMED_ENV=test JOPMED_MYSQL_USER=JOPMED_test JOPMED_MYSQL_PWD=JOPMED_test_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_test_db JOPMED_TYPE_STORAGE=db python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1`
2. Test using the test database:
`JOPMED_ENV=test JOPMED_MYSQL_USER=JOPMED_test JOPMED_MYSQL_PWD=JOPMED_test_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_test_db JOPMED_TYPE_STORAGE=db python3 -m unittest discover tests`
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
