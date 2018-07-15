from tkinter import *
from tkinter import messagebox

from db_tool import DatabaseTool
from settings import Settings
from file_selection_window import FileSelectionWindow

# TODO: Remove the default database string
# TODO: Add keybinding 'Enter' to connect
class ConnectDatabaseWindow(Frame):
	def __init__(self, master: Tk):
		"""
		Window to allow users to connect to a database
		:param master: Root of the layout
		"""
		super().__init__(master=master)
		self.__master = master
		self.__config__()

	def __config__(self):
		"""
		Configure the window display
		:return: None
		"""
		self.__master.resizable(0, 0)

		self.grid(padx=Settings.padding_x, pady=Settings.padding_y)
		self.winfo_toplevel().title('Connect to database')

		# username
		username = Label(master=self, text='Username:', font=Settings.font_small)
		username.grid(row=0, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__username_str = StringVar()
		self.__username_str.set('postgres')
		self.__username_field = Entry(master=self, textvariable=self.__username_str, font=Settings.font_small)
		self.__username_field.grid(row=0, column=1, pady=(0, Settings.padding_y))

		# password
		password = Label(master=self, text='Password:', font=Settings.font_small)
		password.grid(row=1, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__password_str = StringVar()
		self.__password_str.set('root')
		self.__password_field = Entry(master=self, textvariable=self.__password_str, show='*', font=Settings.font_small)
		self.__password_field.grid(row=1, column=1, pady=(0, Settings.padding_y))

		# host
		host = Label(master=self, text='Host:', font=Settings.font_small)
		host.grid(row=2, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__host_str = StringVar()
		self.__host_str.set('localhost')
		self.__host_field = Entry(master=self, textvariable=self.__host_str, font=Settings.font_small)
		self.__host_field.grid(row=2, column=1, pady=(0, Settings.padding_y))

		# port
		port = Label(master=self, text='Port:', font=Settings.font_small)
		port.grid(row=3, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__port_str = StringVar()
		self.__port_str.set('5432')
		self.__port_field = Entry(master=self, textvariable=self.__port_str, font=Settings.font_small)
		self.__port_field.grid(row=3, column=1, pady=(0, Settings.padding_y))

		# database
		database = Label(master=self, text='Database:', font=Settings.font_small)
		database.grid(row=4, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__database_str = StringVar()
		self.__database_str.set('timezonebot')
		self.__database_field = Entry(master=self, textvariable=self.__database_str, font=Settings.font_small)
		self.__database_field.grid(row=4, column=1, pady=(0, Settings.padding_y))

		# connect
		connect = Button(master=self, text='Connect', font=Settings.font_small, command=self.__connect_to_db__)
		connect.grid(row=5, column=1, sticky=E)

	def __connect_to_db__(self):
		"""
		Attempts to connect to the database with the input credentials
		Checks if the database field is empty, or invalid
		If there is a successful connection, then forward to the FileSelectionWindow
		Triggered on button click
		:return: None
		"""
		username = self.__username_field.get()
		password = self.__password_field.get()
		host = self.__host_field.get()
		port = self.__port_field.get()
		database = self.__database_field.get()

		if database == '':
			messagebox.showerror('No database specified',
								 'Please specify a database name to connect to')
		else:
			self.__tool = DatabaseTool(username, password, host, port, database)
			if not self.__tool.has_database():
				messagebox.showerror('Invalid database chosen','The database {} chosen does not exist or the connection details are incorrect.\nRemember that the database name is case-sensitive'.format(database))
			else:
				messagebox.showinfo('Successful connection',
									'You are now connected to the database: {}'.format(database))
				self.__tool.open_engine()
				self.__launch_main_window__()

	def __launch_main_window__(self):
		"""
		Closes the current window and opens the FileSelectionWindow
		:return: None
		"""
		self.__master.destroy()
		FileSelectionWindow(Tk(), self.__tool)

