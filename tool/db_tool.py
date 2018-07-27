from tkinter import messagebox

import pandas as pd
from numpy import ndarray
from pandas import DataFrame
from sqlalchemy import create_engine, MetaData, Column, String, Integer, Float, Boolean, Date, Table
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists

# todo: fix the bug where if the user enters false credentials, the console will spit out error messages for invalid credentials (temporary fix of error messagebox used)
from tool import utils


class DatabaseTool:
	def __init__(self, conn_str: str):
		self.database = utils.extract_db_from_conn_str(conn_str)
		self.__connection_string = conn_str
		self.__engine = None
		self.__Base = None
		self.__meta: MetaData = None

	@staticmethod
	def __create_attr_dict__(tablename: str, headers: dict, df: DataFrame):
		attr_dict = { '__tablename__': tablename }
		for key, value in headers.items():
			dtype_selected = value[0]
			data_type = None
			if dtype_selected == 'int64':
				df[key] = pd.to_numeric(df[key], downcast='integer')
				data_type = Integer
			elif dtype_selected == 'string':
				df[key] = df[key].astype(str)
				max_length = df[key].map(len).max()
				data_type = String(max_length)
			elif dtype_selected == 'float64':
				df[key] = pd.to_numeric(df[key], downcast='float')
				data_type = Float
			elif dtype_selected == 'datetime64':
				df[key] = pd.to_datetime(df[key])
				data_type = Date
			elif dtype_selected == 'bool':
				df[key] = df[key].astype(bool)
				data_type = Boolean

			attr_dict[key] = Column(data_type, primary_key=value[1])

		print(attr_dict)

		return attr_dict

	def __create_table__(self, attr_dict: dict):
		table = type(attr_dict['__tablename__'], (self.__Base,), attr_dict)
		table.extend_existing = True
		self.__meta.create_all(self.__engine)

	def __populate_table__(self, tablename: str, df: DataFrame):
		self.__meta.reflect(bind=self.__engine)
		table: Table = self.__meta.tables[tablename]
		print(type(table))
		with self.__engine.connect() as conn:
			for row in df.values:
				print(row)
				ins = table.insert(values=ndarray.tolist(row))
				conn.execute(ins)

	def has_database(self):
		try:
			database_exists(self.__connection_string)
		except OperationalError:
			messagebox.showerror('Invalid credentials',
								 'The credentials you have entered are invalid, please check to ensure that they are valid ones before proceeding!')

		return database_exists(self.__connection_string)

	def open_engine(self):
		self.__engine = create_engine(self.__connection_string)
		self.__Base = declarative_base(bind=self.__engine)
		self.__meta = self.__Base.metadata

	def get_tables(self):
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
		self.__create_table__(self.__create_attr_dict__(tablename, settings, df))
		self.__populate_table__(tablename, df)
