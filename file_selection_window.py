from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from os import path

from db_tool import DatabaseTool
from settings import Settings
import utils

# TODO: Check the file types and convert accordingly
# TODO: Before converting the file, allow the user to change the data types of the headers
# TODO: Add a field to specify the skip and fill values
class FileSelectionWindow(Frame):
	def __init__(self, master: Tk, db_tool: DatabaseTool):
		"""
		Window to allow the user to select a CSV file
		:param master: Root of the layout
		:param db_tool: Tool that maintains a connection to the database
		"""
		super().__init__(master=master)
		self.__tool = db_tool
		self.__master = master
		self.__config__()


	@staticmethod
	def __is_file_empty__(filename: str):
		"""
		Checks if a file is empty
		:param filename: File to check
		:return: If the file is empty
		"""
		return path.getsize(filename) <= 0

	@staticmethod
	def __is_integer__(target: str):
		"""
		Checks if the target string can be parsed as an integer
		:param target: Target string to test
		:return: If the string is an integer
		"""
		try:
			target = int(target)
		except ValueError:
			return False
		return True

	def __config__(self):
		"""
		Configure the window display
		:return: None
		"""
		self.pack(padx=Settings.padding_x, pady=Settings.padding_y, fill=BOTH)
		self.winfo_toplevel().title('Connected to: {}'.format(self.__tool.database))

		menu = Menu(self)
		menu.add_command(label='View Tables', command=self.__view_tables__)
		self.__master.config(menu=menu)

		# file name
		self.__file_name_str = StringVar()
		self.__file_name_str.set('Nothing is selected')
		self.__file_name_field = Entry(master=self, textvariable=self.__file_name_str, font=Settings.font_small,
									   state=DISABLED)
		self.__file_name_field.pack(fill=X, pady=(0, Settings.padding_y))

		# skiprows
		skiprows_frame = Frame(master=self)
		skiprows_frame.pack(side=TOP, fill=X)
		skiprows = Label(master=skiprows_frame, text='Skip Rows:', font=Settings.font_small)
		skiprows.pack(side=LEFT, padx=(0, Settings.padding_x))
		self.__skiprows_str = StringVar()
		self.__skiprows_str.set(0)
		self.__skiprows_field = Entry(master=skiprows_frame, textvariable=self.__skiprows_str, font=Settings.font_small,
									  state=DISABLED)
		self.__skiprows_field.pack(fill=X)

		# delimiter
		delimiter_frame = Frame(master=self)
		delimiter_frame.pack(fill=X, pady=(Settings.padding_y, 0))
		delimiter = Label(master=delimiter_frame, text='Delimiter:', font=Settings.font_small)
		delimiter.pack(side=LEFT, padx=(0, Settings.padding_x))
		self.__delimiter_str = StringVar()
		self.__delimiter_str.set(',')
		self.__delimiter_field = Entry(master=delimiter_frame,
									   textvariable=self.__delimiter_str,
									   font=Settings.font_small,
									   state=DISABLED)
		self.__delimiter_field.pack(fill=X)

		button_frame = Frame(master=self)
		button_frame.pack(fill=X, pady=(Settings.padding_y, 0))

		# open file
		self.__open_file_button = Button(master=button_frame,
										 text='Open File',
										 font=Settings.font_small,
										 command=self.__open_file__)
		self.__open_file_button.pack(side=LEFT)

		# convert file
		self.__convert_button = Button(master=button_frame,
									   text='Convert',
									   font=Settings.font_small,
									   state=DISABLED,
									   command=self.__convert_file__)
		self.__convert_button.pack(side=RIGHT, padx=(Settings.padding_x, 0))

	def __view_tables__(self):
		"""
		Displays the existing tables in the connected database
		Triggered when menu item selected
		:return: None
		"""
		tables = self.__tool.get_tables()
		to_display = '\n'.join([key for key, value in tables.items()])
		messagebox.showinfo('Existing Tables', to_display)

	def __toggle_states__(self, state):
		"""
		Applies the same state across multiple widgets at once
		:param state: State to be applied
		:return: None
		"""
		self.__convert_button.config(state=state)
		self.__skiprows_field.config(state=state)
		self.__delimiter_field.config(state=state)

	def __open_file__(self):
		"""
		Displays the file select dialog box to allow users to the select the file
		Performs checking to see if the user cancelled the operation since that returns a blank file name
		If the file name is blank, then keep the previous file
		Otherwise, allow the user to customize the skiprows and delimtiers
		:return: None
		"""
		previous_file = self.__file_name_field.get()

		selected_file = filedialog.askopenfilename(
			initialdir="/",
			title="Select file",
			filetypes=[("csv files", "*.csv")])

		if selected_file != '':
			self.__file_name_str.set(selected_file)
			self.__toggle_states__(NORMAL)
			self.__open_file_button.config(text='Change File')
		else:
			if previous_file == 'Nothing is selected':
				self.__toggle_states__(DISABLED)

	def __convert_file__(self):
		"""
		Checks if the inputs for the skiprows and delimiter fields are empty, if they are, the defaults of 0 and , will
		be used respectively
		Checks if the file is empty as well as if the skiprows input is a valid integer
		If successful, it will launch the ConvertSetupWindow to customize the table
		Triggered on button click
		:return: None
		"""
		filename = self.__file_name_field.get()
		skiprows = self.__skiprows_field.get()
		delimiter = self.__delimiter_field.get()

		if skiprows.strip() == '' or delimiter.strip() == '':
			messagebox.showerror('Empty inputs', 'Skip rows and delimiters should not be empty, using defaults of 0 and ,')
			skiprows = '0'
			delimiter = ','

		if self.__is_file_empty__(filename):
			messagebox.showerror('Empty file', 'File: {} is empty, please select another file'.format(filename))
		else:
			if not self.__is_integer__(skiprows):
				messagebox.showerror('Invalid skiprow',
									 'Skiprow: {} is not an integer, please select a valid integer'.format(skiprows))
			else:
				skiprows = int(skiprows)
				utils.launch_setup(self.__master, self.__tool, filename, skiprows, delimiter)