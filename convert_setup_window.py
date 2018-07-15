from tkinter import *
import pandas as pd

from db_tool import DatabaseTool
from settings import Settings

# TODO: Check if the table name is blank, if it is, warn the user to specify one otherwise the file name will be used as the table name
# TODO: Give users the ability to change the skiprows and delimiter
class ConvertSetupWindow(Frame):
	def __init__(self, master: Tk, db_tool: DatabaseTool, filename: str, skiprows: int, delimiter: str):
		super().__init__(master=master)
		self.__filename = filename
		self.__skiprows = skiprows
		self.__delimiter = delimiter

		self.__master = master
		self.__tool = db_tool

		self.__df = self.__open_file__()
		self.__config__()

	def __open_file__(self):
		df = pd.read_csv(self.__filename, skiprows=self.__skiprows, delimiter=self.__delimiter)
		return df

	def __config__(self):
		self.pack(padx=Settings.padding_x, pady=Settings.padding_y, fill=BOTH)
		self.winfo_toplevel().title('Connected to: {}'.format(self.__tool.database))

		# filename
		Label(master=self, text='Converting:', font=Settings.font_medium).pack(anchor=W)
		filename = Label(master=self, text=self.__filename, font=Settings.font_small)
		filename.pack(pady=(0, Settings.padding_y), anchor=W)

		# table name
		tablename_frame = Frame(master=self)
		tablename_frame.pack(fill=X)
		tablename = Label(master=tablename_frame, text='Table Name:', font=Settings.font_small)
		tablename.pack(side=LEFT, padx=(0, Settings.padding_x))
		tablename_str = StringVar()
		tablename_field = Entry(master=tablename_frame, textvariable=tablename_str, font=Settings.font_small)
		tablename_field.pack(fill=X)

		# table headers
		self.__populate_table_headers__()

	def __populate_table_headers__(self):
		for header in self.__df.dtypes:
			print(header)