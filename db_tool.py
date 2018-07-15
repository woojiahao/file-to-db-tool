from pandas import DataFrame
from sqlalchemy import create_engine, MetaData, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists

# TODO: Populate the tables with the corresponding data
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
	def __create_attr_dict__(tablename: str, headers: dict, df: DataFrame):
		attr_dict = { '__tablename__': tablename }
		for key, value in headers.items():
			dtype_selected = value[0]
			data_type = None
			if dtype_selected == 'int64':
				data_type = Integer
			elif dtype_selected == 'string':
				max_length = df[key].map(len).max()
				data_type = String(max_length)
			elif dtype_selected == 'float64':
				data_type = Float

			attr_dict[key] = Column(data_type, primary_key=value[1])

		print(attr_dict)

		return attr_dict

	def __create_table__(self, attr_dict: dict):
		table = type(attr_dict['__tablename__'], (self.__Base,), attr_dict)
		self.__meta.create_all(self.__engine)

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
		print(df.dtypes)
		self.__create_table__(self.__create_attr_dict__(tablename, settings, df))
