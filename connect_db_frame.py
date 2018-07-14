from tkinter import *
from tkinter import messagebox

from settings import Settings
from db_tool import DatabaseTool


class ConnectDbFrame(Frame):
	"""Provides the user with the ability to connect to a database of their choice"""

	def __init__(self, master: Tk):
		super().__init__(master=master)
		self.__master = master
		self.__config__()

	def __config__(self):
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
		self.__database_field = Entry(master=self, textvariable=self.__database_str, font=Settings.font_small)
		self.__database_field.grid(row=4, column=1, pady=(0, Settings.padding_y))

		# connect
		connect = Button(master=self, text='Connect', font=Settings.font_small, command=self.__connect_to_db__)
		connect.grid(row=5, column=1, sticky=E)

	def __connect_to_db__(self):
		username = self.__username_field.get()
		password = self.__password_field.get()
		host = self.__host_field.get()
		port = self.__port_field.get()
		database = self.__database_field.get()

		if database == '':
			messagebox.showerror('No database specified', 'Please specify a database name to connect to')
		else:
			tool = DatabaseTool(username, password, host, port, database)

root = Tk()

connect_db = ConnectDbFrame(root)

if __name__ == '__main__':
	root.mainloop()
