from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

import pandas as pd
from pandas import DataFrame

from db_tool import DatabaseTool
from settings import Settings
import utils

# TODO: Give users the ability to change the skiprows and delimiter
# TODO: Fix the table name field and label not being on the same line
# TODO: Add field heading
# TODO: Add confirmation dialog before converting
# TODO: Allow users to change the name of the columns
class ConvertSetupWindow(Frame):
	def __init__(self, master: Tk, db_tool: DatabaseTool, filename: str, skiprows: int, delimiter: str):
		"""
		This window will allow users to configure the table that will be created
		Specify the data type of the column, the name of the column and whether the column will be a PK
		:param master: Root of the layout
		:param db_tool: Tool that maintains a connection to the database
		:param filename: Name of the file to convert
		:param skiprows: Skip rows parameter for reading the CSV
		:param delimiter: Delimiter that separates each entry in the CSV file
		"""
		super().__init__(master=master)
		self.__filename = filename
		self.__skiprows = skiprows
		self.__delimiter = delimiter

		self.__dtypes = [
			'string', 'int64', 'float64',
			'bool', 'datetime64'
		]

		self.__master = master
		self.__tool = db_tool

		self.__df: DataFrame = self.__open_file__()
		self.__config__()

	def __open_file__(self):
		"""
		Simple method that uses pandas to open the specified CSV file
		:return: DataFrame of the target CSV file
		"""
		df = pd.read_csv(self.__filename, skiprows=self.__skiprows, delimiter=self.__delimiter)
		return df

	def __config__(self):
		"""
		Configures the window display
		:return:
		"""
		self.pack(padx=Settings.padding_x, pady=Settings.padding_y, fill=BOTH)
		self.winfo_toplevel().title('Connected to: {}'.format(self.__tool.database))

		menu = Menu(master=self)
		menu.add_command(label='Drop All Tables', command=self.__drop_tables__)
		self.__master.config(menu=menu)

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
		self.__tablename_field = Entry(master=tablename_frame, textvariable=tablename_str, font=Settings.font_small)
		self.__tablename_field.pack(fill=X, pady=(0, Settings.padding_y))

		# table headers
		self.__headers = Frame(master=self)
		self.__headers.pack(fill=X)
		self.__populate_table_headers__()

		button_frame = Frame(master=self)
		button_frame.pack(anchor=E)

		# reset button
		reset_button = Button(master=button_frame, text='Reset', font=Settings.font_small,
							  command=self.__reset_fields__)
		reset_button.grid(row=0, column=0, padx=(0, Settings.padding_x))

		# convert button
		convert_button = Button(master=button_frame, text='Convert', font=Settings.font_small, command=self.__convert__)
		convert_button.grid(row=0, column=1)

	def __populate_table_headers__(self):
		"""
		Goes through every column within the dataframe and dynamically generates the column editing "row" inside the
		header frame.
		Maintains a copy of the primary key BooleanVars as it has to be used later on again
		:return: None
		"""
		self.__pks = []
		for col_name, col_type in zip(self.__df.columns.values, self.__df.dtypes):
			inline_frame = Frame(master=self.__headers)
			inline_frame.pack(fill=X, pady=(0, Settings.padding_y))

			col_name_str = StringVar()
			col_name_str.set(col_name)
			col_name_field = Entry(master=inline_frame, textvariable=col_name_str, font=Settings.font_small, state=DISABLED)
			col_name_field.grid(row=0, column=0, padx=(0, Settings.padding_x))

			col_type_selection = Combobox(master=inline_frame,
										  value=self.__dtypes,
										  font=Settings.font_small,
										  state="readonly")
			col_type_selection.set(col_type if col_type != 'object' else 'string')
			col_type_selection.grid(row=0, column=1, padx=(0, Settings.padding_x))

			pk = BooleanVar()
			primary_key_check = Checkbutton(master=inline_frame, text='PK', font=Settings.font_small,
											variable=pk)
			primary_key_check.grid(row=0, column=2)
			self.__pks.append(pk)

	def __drop_tables__(self):
		"""
		Drops all of the tables in the database
		Triggered on menu item press
		:return: None
		"""
		self.__tool.drop_tables()
		messagebox.showinfo('All tables dropped', 'All tables have been dropped successfully!')

	def __reset_fields__(self):
		pass

	def __is_valid_pk__(self, headers: dict):
		"""
		Valid primary key can be composed of multiple columns
		Join all the selected columns together into a column
		A valid combination of PK when the length of the normal joint column is == to the length of the distinct column
		:param headers: Column data
		:return: If the combination of PKs are valid.
		"""
		pks = [key for key, value in headers.items() if value[1]]
		filtered = self.__df[pks[0]].map(str)

		for i in range(1, len(pks)):
			filtered += self.__df[pks[i]].map(str)

		length = len(filtered)
		d_length = len(set(filtered))

		return length == d_length

	@staticmethod
	def __check_pk__(headers: dict):
		"""
		Checks whether at least 1 column is selected to be the PK
		Uses boolean algebra to determine if there is a PK selected
		:param headers: Column data
		:return: If there is a PK selected
		"""
		has_pk = False
		for value in headers.values():
			has_pk |= value[1]
		return has_pk

	def __get_all_values__(self):
		"""
		Loops through the headers (column editing) section widgets
		Goes through each of the children of each row and extracts the data from it
		Creates a dictionary where the keys are the column names and the values is a list => [<data_type>, <is_pk>]
		:return: Dictionary of the column information needed to form an attr_dict
		"""
		rows = { }
		key = ''
		for i, row in enumerate(self.__headers.winfo_children()):
			for j, child in enumerate(row.winfo_children()):
				if j == 0 and type(child) is Entry:
					key = child.get()
					rows[key] = []
				else:
					if type(child) is Entry or type(child) is Combobox:
						print(child.get())
						rows[key].append(child.get())
					elif type(child) is Checkbutton:
						rows[key].append(self.__pks[i].get())
		return rows

	def __convert__(self):
		"""
		Attempts to convert the input CSV file to a database table
		Toggled on button click
		Performs checks for empty table names, invalid combinations of PKs and no PKs being selected.
		:return: None
		"""
		table_name = self.__tablename_field.get()
		if table_name.strip() == '':
			messagebox.showerror('Empty table name', 'You did not specify a table name!')
		else:
			headers = self.__get_all_values__()
			if not self.__check_pk__(headers):
				messagebox.showerror('No Primary Key', 'You did not select any primary keys')
			else:
				if not self.__is_valid_pk__(headers):
					messagebox.showerror('Invalid Primary Key',
										 'The primary key(s) you selected is invalid as there are repeating values')
				else:
					messagebox.showinfo('Converting file to table!',
										'The file: {} is currently being converted to a table!'.format(self.__filename))
					self.__tool.convert(self.__df, table_name, headers)
					utils.launch_file_selection(self.__master, self.__tool)