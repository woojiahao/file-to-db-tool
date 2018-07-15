from pandas import DataFrame
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists


class DatabaseTool:
	def __init__(self, username: str, password: str, host: str, port: str, database: str):
		self.database = database
		self.__connection_string = self.__create_connection_string__(username, password, host, port, database)
		self.__engine = None
		self.__Base = None
		self.__meta: MetaData = None

	@staticmethod
	def __create_connection_string__(username: str, password: str, host: str, port: str, database: str):
		return 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, database)

	@staticmethod
	def __create_attr_dict__(tablename: str, headers: dict):
		attr_dict = { '__tablename__': tablename }
		return attr_dict

	def __create_table__(self, attr_dict: dict):
		pass

	def has_database(self):
		return database_exists(self.__connection_string)

	def open_engine(self):
		self.__engine = create_engine(self.__connection_string)
		self.__Base = declarative_base(bind=self.__engine)
		self.__meta = self.__Base.metadata

	def get_tables(self):
		self.__meta.reflect(bind=self.__engine)
		tables = self.__meta.tables
		return tables

	def convert(self, df: DataFrame, tablename: str, settings: dict):
		self.__create_table__(self.__create_attr_dict__(tablename, settings))
