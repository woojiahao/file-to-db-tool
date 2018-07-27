from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import re

from tool import utils
from tool.connection_string_popup import ConnectionStringPopup
from tool.db_tool import DatabaseTool
from tool.settings import Settings


# todo: allow users the ability to edit the config.json file within the application instead of having to manually change it
# todo: allow users to specify a whole connection string separately without specifying the individual credentials
# todo: allow for an option for ssl connection mode
class ConnectDatabaseWindow(Frame):
	def __init__(self, master: Tk):
		super().__init__(master=master)
		self.__master = master
		self.__config__()

	def __config__(self):
		self.__master.resizable(0, 0)
		self.grid(padx=Settings.padding_x, pady=Settings.padding_y)
		self.winfo_toplevel().title('Connect to database')

		def key(event):
			self.__connect_to_db__()

		self.__master.bind('<Return>', key)

		menu = Menu(master=self)
		menu.add_command(label='Specify Connection String', command=self.__specify_connection_string__)
		self.__master.config(menu=menu)

		# select dialect drop down
		self.__available_dialects = utils.read_configuration_file('config.json')
		dialects = Label(master=self, text='Dialect:', font=Settings.font_small)
		dialects.grid(row=0, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__dialects_selection = Combobox(master=self,
											 values=list(self.__available_dialects.keys()),
											 font=Settings.font_small,
											 state="readonly")
		self.__dialects_selection.set(list(self.__available_dialects.keys())[0])
		self.__dialects_selection.bind('<<ComboboxSelected>>', self.__cbox_item_selected__)
		self.__dialects_selection.grid(row=0, column=1, pady=(0, Settings.padding_y))

		# username
		username = Label(master=self, text='Username:', font=Settings.font_small)
		username.grid(row=1, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__username_str = StringVar()
		self.__username_str.set(self.__available_dialects['postgresql']['username'])
		self.__username_field = Entry(master=self, textvariable=self.__username_str, font=Settings.font_small)
		self.__username_field.grid(row=1, column=1, pady=(0, Settings.padding_y))

		# password
		password = Label(master=self, text='Password:', font=Settings.font_small)
		password.grid(row=2, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__password_str = StringVar()
		self.__password_str.set(self.__available_dialects['postgresql']['password'])
		self.__password_field = Entry(master=self, textvariable=self.__password_str, show='*', font=Settings.font_small)
		self.__password_field.grid(row=2, column=1, pady=(0, Settings.padding_y))

		# host
		host = Label(master=self, text='Host:', font=Settings.font_small)
		host.grid(row=3, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__host_str = StringVar()
		self.__host_str.set(self.__available_dialects['postgresql']['host'])
		self.__host_field = Entry(master=self, textvariable=self.__host_str, font=Settings.font_small)
		self.__host_field.grid(row=3, column=1, pady=(0, Settings.padding_y))

		# port
		port = Label(master=self, text='Port:', font=Settings.font_small)
		port.grid(row=4, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__port_str = StringVar()
		self.__port_str.set(self.__available_dialects['postgresql']['port'])
		self.__port_field = Entry(master=self, textvariable=self.__port_str, font=Settings.font_small)
		self.__port_field.grid(row=4, column=1, pady=(0, Settings.padding_y))

		# database
		database = Label(master=self, text='Database:', font=Settings.font_small)
		database.grid(row=5, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__database_str = StringVar()
		self.__database_field = Entry(master=self, textvariable=self.__database_str, font=Settings.font_small)
		self.__database_field.grid(row=5, column=1, pady=(0, Settings.padding_y))

		# connect
		connect = Button(master=self, text='Connect', font=Settings.font_small, command=self.__connect_to_db__)
		connect.grid(row=6, column=1, sticky=E)

	def __specify_connection_string__(self):
		popup = ConnectionStringPopup(self)
		conn_str = popup.conn_str
		self.__connect_to_db__(conn_str=conn_str)

	def __cbox_item_selected__(self, event):
		selected = self.__dialects_selection.get()
		credentials = self.__available_dialects[selected]
		self.__set_credentials__(credentials)

	def __set_credentials__(self, credentials: dict):
		utils.set_entry_text(self.__username_field, credentials['username'])
		utils.set_entry_text(self.__password_field, credentials['password'])
		utils.set_entry_text(self.__host_field, credentials['host'])
		utils.set_entry_text(self.__port_field, credentials['port'])

	def __get_connection_details__(self):
		username = self.__username_field.get()
		password = self.__password_field.get()
		host = self.__host_field.get()
		port = self.__port_field.get()
		database = self.__database_field.get()
		dialect = self.__dialects_selection.get()
		dialect_str = '{}+{}'.format(dialect, self.__available_dialects[dialect]['connector'])

		return {
			'username': username,
			'password': password,
			'host': host,
			'port': port,
			'database': database,
			'dialect_str': dialect_str
		}

	def __connect_to_db__(self, conn_str: str = None):
		connection: str = ''
		if conn_str is not None:
			pattern = '^\w+:\/\/\w+:\w+\@\w+:\d+\/\w+$'
			if re.match(pattern, conn_str) is None:
				messagebox.showerror('Invalid connection string format',
									 'The connection string you entered: {} is in an invalid format, please try again'.format(conn_str))
			else:
				connection = conn_str
		else:
			conn_details = self.__get_connection_details__()

			if conn_details['database'] == '':
				messagebox.showerror('No database specified',
									 'Please specify a database name to connect to')
			else:
				connection = utils.create_connection_string(
					conn_details['username'],
					conn_details['password'],
					conn_details['host'],
					conn_details['port'],
					conn_details['database'],
					conn_details['dialect_str'])

		self.__tool = DatabaseTool(connection)
		database_name = utils.extract_db_from_conn_str(connection)
		if not self.__tool.has_database():
			messagebox.showerror('Invalid database chosen',
								 'The database {} chosen does not exist or the connection details are incorrect.\nRemember that the database name is case-sensitive'.format(
									 database_name))
		else:
			messagebox.showinfo('Successful connection',
								'You are now connected to the database: {}'.format(database_name))
			self.__tool.open_engine()
			utils.launch_file_selection(self.__master, self.__tool)
