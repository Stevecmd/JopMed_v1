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
`JOPMED_ENV=test JOPMED_MYSQL_USER=JOPMED_test JOPMED_MYSQL_PWD=JOPMED_test_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_test_db JOPMED_TYPE_STORAGE=db python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1`

- Improve storage
`JOPMED_MYSQL_USER=JOPMED_dev JOPMED_MYSQL_PWD=JOPMED_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_dev_db JOPMED_TYPE_STORAGE=db ./test_get_count.py`

- Status of your API
`JOPMED_MYSQL_USER=JOPMED_dev JOPMED_MYSQL_PWD=JOPMED_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_dev_db JOPMED_TYPE_STORAGE=db JOPMED_API_HOST=0.0.0.0 JOPMED_API_PORT=5000 python3 -m api.v1.app`

`curl -X GET http://0.0.0.0:5000/api/v1/status`

- Some stats?
`curl -X GET http://0.0.0.0:5000/api/v1/stats`

- Not found
`curl -X GET http://0.0.0.0:5000/api/v1/nop`
`curl -X GET http://0.0.0.0:5000/api/v1/nop -vvv`

- State
`curl -X GET http://0.0.0.0:5000/api/v1/states/`


0x06
- Cash only
`JOPMED_MYSQL_USER=JOPMED_dev JOPMED_MYSQL_PWD=JOPMED_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_dev_db JOPMED_TYPE_STORAGE=db python3 -m web_dynamic.0-JOPMED`

- API status
`JOPMED_MYSQL_USER=JOPMED_dev JOPMED_MYSQL_PWD=JOPMED_dev_pwd JOPMED_MYSQL_HOST=localhost JOPMED_MYSQL_DB=JOPMED_dev_db JOPMED_TYPE_STORAGE=db JOPMED_API_PORT=5001 python3 -m api.v1.app`

Automatically update the `requirements.txt` file:
`pip freeze > requirements.txt`
