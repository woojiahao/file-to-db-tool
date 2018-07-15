from tkinter import *
import pandas as pd
from pandas import DataFrame

from db_tool import DatabaseTool
from settings import Settings

# TODO: Check if the table name is blank, if it is, warn the user to specify one otherwise the file name will be used as the table name
# TODO: Give users the ability to change the skiprows and delimiter
# TODO: Add checking if the intended PKs can be used as PKs
# TODO: Fix the table name field and label not being on the same line
class ConvertSetupWindow(Frame):
	def __init__(self, master: Tk, db_tool: DatabaseTool, filename: str, skiprows: int, delimiter: str):
		super().__init__(master=master)
		self.__filename = filename
		self.__skiprows = skiprows
		self.__delimiter = delimiter

		self.__master = master
		self.__tool = db_tool

		self.__df: DataFrame = self.__open_file__()
		self.__config__()

	def __open_file__(self):
		df = pd.read_csv(self.__filename, skiprows=self.__skiprows, delimiter=self.__delimiter)
		return df

	def __config__(self):
		self.pack(padx=Settings.padding_x, pady=Settings.padding_y, fill=BOTH)
		self.winfo_toplevel().title('Connected to: {}'.format(self.__tool.database))

		# filename
		Label(master=self, text='Converting:', font=Settings.font_medium).pack(anchor=W)
		filename_str = StringVar()
		filename_str.set(self.__filename)
		filename_field = Entry(master=self, textvariable=filename_str, font=Settings.font_small, state=DISABLED)
		filename_field.pack(pady=(0, Settings.padding_y), anchor=W, fill=X)

		# table name
		tablename_frame = Frame(master=self)
		tablename_frame.pack(fill=X)
		tablename = Label(master=tablename_frame, text='Table Name:', font=Settings.font_small)
		tablename.pack(side=LEFT, padx=(0, Settings.padding_x))
		tablename_str = StringVar()
		tablename_field = Entry(master=tablename_frame, textvariable=tablename_str, font=Settings.font_small)
		tablename_field.pack(fill=X, pady=(0, Settings.padding_y))

		# table headers
		self.__populate_table_headers__()

	def __populate_table_headers__(self):
		for col_name, col_type in zip(self.__df.columns.values, self.__df.dtypes):
			print('col_name: {}\ncol_type: {}\n'.format(col_name, col_type))

			inline_frame = Frame(master=self)
			inline_frame.pack(fill=X, pady=(0, Settings.padding_y))

			col_name_str = StringVar()
			col_name_str.set(col_name)
			col_name_field = Entry(master=inline_frame, textvariable=col_name_str, font=Settings.font_small)
			col_name_field.grid(row=0, column=0, padx=(0, Settings.padding_x))

			col_type_str = StringVar()
			col_type_str.set(col_type)
			col_type_field = Entry(master=inline_frame, textvariable=col_type_str, font=Settings.font_small)
			col_type_field.grid(row=0, column=1, padx=(0, Settings.padding_x))

			primary_key_check = Checkbutton(master=inline_frame, text='PK', font=Settings.font_small, variable=BooleanVar())
			primary_key_check.grid(row=0, column=2)

