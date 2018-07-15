from pandas import DataFrame
from sqlalchemy import create_engine, MetaData, Column, String, Integer, Float, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists

# TODO: Populate the tables with the corresponding data
class DatabaseTool:
	def __init__(self, username: str, password: str, host: str, port: str, database: str):
		"""
		Maintains a connection to the database and provides database-related functions
		:param username: Username for connection string
		:param password: Password for connection string
		:param host: Host for connection string
		:param port: Port number for connection string
		:param database: Database name for connection string
		"""
		self.database = database
		self.__connection_string = self.__create_connection_string__(username, password, host, port, database)
		self.__engine = None
		self.__Base = None
		self.__meta: MetaData = None
		self.__Session = None

	@staticmethod
	def __create_connection_string__(username: str, password: str, host: str, port: str, database: str):
		"""
		Creates the connection string from the input variables
		:param username: Username for connection string
		:param password: Password for connection string
		:param host: Host for connection string
		:param port: Port number for connection string
		:param database: Database name for connection string
		:return: Connection string in proper format
		"""
		return 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, database)

	@staticmethod
	def __create_attr_dict__(tablename: str, headers: dict, df: DataFrame):
		"""
		Generates an attribute dictionary for the soon to be created table
		:param tablename: Name of the table
		:param headers: Column data
		:param df: Data frame of the CSV file
		:return: An attribute dictionary
		"""
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
			elif dtype_selected == 'datetime64':
				data_type = Date
			elif dtype_selected == 'bool':
				data_type = Boolean

			attr_dict[key] = Column(data_type, primary_key=value[1])

		print(attr_dict)

		return attr_dict

	def __create_table__(self, attr_dict: dict):
		"""
		Creates the table based on the attr_dict
		:param attr_dict: Format of the table
		:return: None
		"""
		table = type(attr_dict['__tablename__'], (self.__Base,), attr_dict)
		table.extend_existing = True
		self.__meta.create_all(self.__engine)

	def __populate_table__(self, tablename: str, df: DataFrame):
		pass

	def has_database(self):
		"""
		Checks if the database in the connection string is a valid name
		:return: Whether the database exists
		"""
		return database_exists(self.__connection_string)

	def open_engine(self):
		"""
		Establishes a successful connection and initalizes all the ORM related stuff
		:return: None
		"""
		self.__engine = create_engine(self.__connection_string)
		self.__Base = declarative_base(bind=self.__engine)
		self.__meta = self.__Base.metadata
		self.__Session = sessionmaker(bind=self.__engine)

	def get_tables(self):
		"""
		Relies on metadata to pull the names of the existing tables in the database
		:return: A list of the table names from the database
		"""
		self.__meta.reflect(bind=self.__engine)
		tables = self.__meta.tables
		return tables

	def has_table(self, tablename: str):
		self.__meta.reflect(bind=self.__engine)
		try:
			self.__meta.tables[tablename]
		except KeyError:
			return False
		return True

	def convert(self, df: DataFrame, tablename: str, settings: dict):
		"""
		Converts a CSV file to a database table
		:param df: DataFrame of the CSV file
		:param tablename: Table name
		:param settings: Column data
		:return: None
		"""
		print(df.dtypes)
		self.__create_table__(self.__create_attr_dict__(tablename, settings, df))
		self.__populate_table__(tablename, df)
