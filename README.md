# file-to-db-tool
A GUI tool that reads a file and converts the file into a database table.

## Libraries used:
1. pandas
2. sqlalchemy
3. tkinter
4. psycopg2
5. sqlalchemy_utils

## Database set-up guide 
This repository is able to run both on a local machine and on a server hosted on a service like Heroku. This can be done since the program allows you to specify the connection string information beforehand, thus allowing you to customize the manner in which you will be able to connect to.

![alt text](https://github.com/woojiahao/file-to-db-tool/blob/master/screenshots/connect_db.PNG "Connection Screen")

The following guides will be for both running this application on a local machine and running on a server, hosted on Heroku.

### Local machine:
1. Install [PostgreSQL](https://www.postgresql.org/download/windows/) onto your local machine and include the program `pgAdmin4`.
2. Next, create a new database instance, naming it anything, using `CREATE DATABASE <anything>`
3. After that, run the tool via `python launch.py`.
4. Then, specify the host name (`localhost`), database name (whatever you chose), username (`postgres` is the default), password (`root` is the default) and port number (`5432` is the default) in the tool's connect to database window.

## Set-up guide (for Heroku):
1. Create a free tier [Heroku account](https://signup.heroku.com/?c=70130000001x9jFAAQ).
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
3. Create a GitHub repository, private or not, it does not matter. (In this instance, I made a private one)
4. Clone the repository onto your local machine and `cd` into it.
5. Run the command `heroku create`.
6. Add a `Procfile` to the base folder.
7. Run the `heroku config` command, you should see an automatically generated `DATABASE_URL` [environment variable](https://devcenter.heroku.com/articles/config-vars). If there isn't such an environment variable, 

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