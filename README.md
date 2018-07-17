# file-to-db-tool
A GUI tool that reads a file and converts the file into a database table.

## Database set-up guide 
This repository is able to run both on a local machine and on a server hosted on a service like Heroku. This can be done since the program allows you to specify the connection string information beforehand, thus allowing you to customize the manner in which you will be able to connect to.

![alt text](https://github.com/woojiahao/file-to-db-tool/blob/master/screenshots/connect_db.PNG "Connection Screen")

The following guides will be for both running this application on a local machine and running on a server, hosted on Heroku.

**Note! Heroku's free tier can only support up till 10,000 rows in the database. If you wish to convert `.csv` files with more than 10,000 rows of data, you must either, a) purchase a higher plan, b) use a local database instead**

### Local machine:
1. Install [PostgreSQL](https://www.postgresql.org/download/windows/) onto your local machine and include the program `pgAdmin4`.
2. Next, create a new database instance, naming it anything, using `CREATE DATABASE <anything>`
3. After that, run the tool via `python launch.py`.
4. Then, specify the host name (`localhost`), database name (whatever you chose), username (`postgres` is the default), password (`root` is the default) and port number (`5432` is the default) in the tool's connect to database window.
5. Press on connect and you can now freely use the tool.

### Heroku:
1. Create a free tier [Heroku account](https://signup.heroku.com/?c=70130000001x9jFAAQ).
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
3. Create a GitHub repository, private or not, it does not matter. 
4. Clone the repository onto your local machine and `cd` into it.
5. Run the command `heroku create`, running this command will randomly assign an instance name for your project, you can specify a name for your instance in the same command `heroku create <instance name>`.
6. To verify that the instance was created properly, run the command `git remote -v`, you should see that there will be a new remote added to your project with the Git repository being a Git repository managed by Heroku.
7. Add a `Procfile` to the base folder.
8. Then, log in to Heroku and find your instance name for the Git repository and click into it. 
9. Under the `Resources` tab, you will see a section for `Add-Ons` and you should see `Heroku Postgres :: Database`. If that is not availale for you, return to the command line and enter the following code: `heroku addons:create heroku-postgresql:hobby-dev`. Then refresh the browser page and check if it's added.
10. Click into the add-on and you will be greeted with a datastore, to find the database instance credentials, go under `Settings` and click on the button `View Credentials`.
11. Take note of the **host name**, **username**, **password** and **port number** and **database**.
15. Run the tool using `python launch.py` and populate the fields in the connect screen with the credentials previously mentioned.
16. Press `Connect` and you should be able to access the database and convert `.csv` files now.

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