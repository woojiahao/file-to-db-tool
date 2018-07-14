from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
import pandas as pd


class DatabaseTool:
	def __init__(self, username: str, password: str, host: str, port: str, database: str):
		self.database = database
		self.__connection_string = self.__create_connection_string__(username, password, host, port, database)
		self.__engine = None

	@staticmethod
	def __create_connection_string__(username: str, password: str, host: str, port: str, database: str):
		return 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, database)


	def has_database(self):
		return database_exists(self.__connection_string)

	def open_engine(self):
		self.__engine = create_engine(self.__connection_string)

	def convert(self, filename: str, skiprows: int, delimiter: str):
		df = pd.read_csv(filename, skiprows=skiprows, delimiter=delimiter)
		print(df)

