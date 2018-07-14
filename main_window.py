from tkinter import *

from db_tool import DatabaseTool
from settings import Settings


class MainWindow(Frame):
	def __init__(self, master: Tk, db_tool: DatabaseTool):
		super().__init__(master=master)
		self.__tool = db_tool
		self.__config__()

	def __config__(self):
		self.pack(padx=Settings.padding_x, pady=Settings.padding_y, fill=BOTH)
		self.winfo_toplevel().title('Connected to: {}'.format(self.__tool.database))

		# file name
		file_name_str = StringVar()
		file_name_str.set('Nothing is selected')
		file_name_field = Entry(master=self, textvariable=file_name_str, font=Settings.font_small, state=DISABLED)
		file_name_field.pack(fill='x', pady=(0, Settings.padding_y))

		# skiprows
		skiprows_frame = Frame(master=self)
		skiprows_frame.pack(side=TOP, fill=X)
		skiprows = Label(master=skiprows_frame, text='Skip Rows:', font=Settings.font_small)
		skiprows.pack(side=LEFT, padx=(0, Settings.padding_x))
		skiprows_str = StringVar()
		skiprows_str.set(0)
		skiprows_field = Entry(master=skiprows_frame, textvariable=skiprows_str, font=Settings.font_small, state=DISABLED)
		skiprows_field.pack(fill=X)

		# delimiter
		delimiter_frame = Frame(master=self)
		delimiter_frame.pack(fill=X, pady=(Settings.padding_y, 0))
		delimiter = Label(master=delimiter_frame, text='Delimiter:', font=Settings.font_small)
		delimiter.pack(side=LEFT, padx=(0, Settings.padding_x))
		delimiter_str = StringVar()
		delimiter_str.set(',')
		delimiter_field = Entry(master=delimiter_frame, textvariable=delimiter_str, font=Settings.font_small, state=DISABLED)
		delimiter_field.pack(fill=X)

		button_frame = Frame(master=self)
		button_frame.pack(fill=X, pady=(Settings.padding_y, 0))

		# open file
		open_file_button = Button(master=button_frame, text='Open File', font=Settings.font_small, command=self.__open_file__)
		open_file_button.grid(column=0)

		# convert file
		convert_button = Button(master=button_frame, text='Convert', font=Settings.font_small, state=DISABLED)
		convert_button.grid(row=0, column=1, padx=(Settings.padding_x, 0))

	def __open_file__(self):
		print('Opening file')
