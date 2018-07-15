from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from os import path

from db_tool import DatabaseTool
from settings import Settings
from convert_setup_window import ConvertSetupWindow

# TODO: Check the file types and convert accordingly
# TODO: Before converting the file, allow the user to change the data types of the headers
class FileSelectionWindow(Frame):
	def __init__(self, master: Tk, db_tool: DatabaseTool):
		super().__init__(master=master)
		self.__tool = db_tool
		self.__master = master
		self.__config__()

	def __config__(self):
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
		tables = self.__tool.get_tables()
		to_display = '\n'.join([key for key, value in tables.items()])
		messagebox.showinfo('Existing Tables', to_display)

	def __toggle_states__(self, state):
		self.__convert_button.config(state=state)
		self.__skiprows_field.config(state=state)
		self.__delimiter_field.config(state=state)

	def __open_file__(self):
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


	def __is_file_empty__(self, filename: str):
		return path.getsize(filename) <= 0

	def __is_integer__(self, target: str):
		try:
			target = int(target)
		except ValueError:
			return False
		return True

	def __convert_file__(self):
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
				self.__launch_setup_window__(filename, skiprows, delimiter)

	def __launch_setup_window__(self, filename: str, skiprows: int, delimiter: str):
		self.__master.destroy()
		ConvertSetupWindow(Tk(), self.__tool, filename, skiprows, delimiter)
