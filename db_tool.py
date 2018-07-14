from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists
from tkinter import messagebox

class DatabaseTool:
	def __init__(self, username: str, password: str, host: str, port: str, database: str):
		connection_string = self.__create_connection_string__(username, password, host, port, database)

		if not database_exists(connection_string):
			messagebox.showerror('Invalid database chosen',
								 'The database {} chosen does not exist, please select another one'.format(database))
		else:
			print('connected')
			self.__engine = create_engine(connection_string)

	@staticmethod
	def __create_connection_string__(username: str, password: str, host: str, port: str, database: str):
		return 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, database)
