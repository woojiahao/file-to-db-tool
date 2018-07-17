# file-to-db-tool
A GUI tool that reads a file and converts the file into a database table.

## Database set-up guide 
This tool is able to run the code off any database, be it locally or on another server, you simply have to specify these details at the connect screen.

### Currently supported SQL Dialects:
1. PostgreSQL

![alt text](https://github.com/woojiahao/file-to-db-tool/blob/master/screenshots/connect_db.PNG "Connection Screen")

### Local machine:
1. Install [PostgreSQL](https://www.postgresql.org/download/windows/) onto your local machine and include the program `pgAdmin4`.
2. Next, create a new database instance, naming it anything, using `CREATE DATABASE <anything>`
3. After that, run the tool via `python launch.py`.
4. Then, specify the host name (`localhost`), database name (whatever you chose), username (`postgres` is the default), password (`root` is the default) and port number (`5432` is the default) in the tool's connect to database window.
5. Press on connect and you can now freely use the tool.

## Libraries used:
1. pandas
2. sqlalchemy
3. tkinter
4. psycopg2
5. sqlalchemy_utils

## Usage guide:
1. Ensure that you have all the libraries used installed on your machine, if you don't install them with the following commands:
```bash
pip install pandas
pip install sqlalchemy
pip install psycopg2
pip install sqlalchemy_utils
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

## Supported file types:
* `.csv`

## TODO:
1. Allow the user the dialect of SQL that they want to use, MySQL vs PostgreSQL
2. Allow the user to enter a connection string rather than breaking everything up themselves
3. Add screenshots for the instructions