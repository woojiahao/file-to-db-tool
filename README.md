# File to Database Table Conversion Tool
A GUI tool that reads a file and converts the file into a database table.

This tool emphasises on flexibility, allowing you to connect to any database by specifying the needed credentials.

![alt text](https://github.com/woojiahao/file-to-db-tool/blob/master/screenshots/connect_db.PNG "Connection Screen")

## Libraries used:
1. pandas
2. sqlalchemy
3. tkinter
4. psycopg2
5. pymysql
6. sqlalchemy_utils

## Usage guide:
1. Ensure that you have all the libraries used installed on your machine, if you don't install them with the following commands:
```bash
pip install pandas
pip install sqlalchemy
pip install psycopg2
pip install sqlalchemy_utils
pip install pymysql
```
2. Download/Clone/Fork this repository to your local machine
3. Navigate to the folder
4. Run `launch.py`
```bash
cd Desktop
git clone https://github.com/woojiahao/file-to-db-tool
cd file-to-db-tool
python launch.py
```
5. When the program has launched, select the dialect of SQL you will be using (See [Available SQL Dialects](https://github.com/woojiahao/file-to-db-tool#currently-supported-sql-dialects)).
6. By selecting them, it will automaticaly fill in the credentials needed for a localhost conenction to that database, feel free to edit the credentials if you need to conenct to an external database.
7. Enter the database name that you wish to connect to and press `Connect`.
8. Select a supported file (See [Supported File Types](https://github.com/woojiahao/file-to-db-tool#supported-file-types)) and convert.


## Available SQL Dialects:
1. PostgreSQL
2. MySQL

## Supported file types:
* `.csv`

## TODO:
1. Allow the user to enter a connection string rather than breaking everything up themselves
2. Add screenshots for the instructions