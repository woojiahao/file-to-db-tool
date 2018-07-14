from tkinter import *
from settings import Settings

class ConnectDbWindow:
	"""Provides the user with the ability to connect to a database of their choice"""
	def __init__(self, master: Tk):
		self.__master = master
		self.__config__()

	def __config__(self):
		self.__master.resizable(0, 0)

		frame = Frame(master=self.__master)
		frame.grid(padx=Settings.padding_x, pady=Settings.padding_y)
		frame.winfo_toplevel().title('Connect to database')

		# username
		username = Label(master=frame, text='Username:', font=Settings.font_small)
		username.grid(row=0, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__username_field = Entry(master=frame, font=Settings.font_small)
		self.__username_field.grid(row=0, column=1, pady=(0, Settings.padding_y))

		# password
		password = Label(master=frame, text='Password:', font=Settings.font_small)
		password.grid(row=1, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__password_field = Entry(master=frame, font=Settings.font_small)
		self.__password_field.grid(row=1, column=1, pady=(0, Settings.padding_y))

		# port
		port = Label(master=frame, text='Port:', font=Settings.font_small)
		port.grid(row=2, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__port_field = Entry(master=frame, font=Settings.font_small)
		self.__port_field.grid(row=2, column=1, pady=(0, Settings.padding_y))

		# host
		host = Label(master=frame, text='Host:', font=Settings.font_small)
		host.grid(row=3, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__host_field = Entry(master=frame, font=Settings.font_small)
		self.__host_field.grid(row=3, column=1, pady=(0, Settings.padding_y))

		# database
		database = Label(master=frame, text='Database:', font=Settings.font_small)
		database.grid(row=4, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		self.__database_field = Entry(master=frame, font=Settings.font_small)
		self.__database_field.grid(row=4, column=1, pady=(0, Settings.padding_y))

		# connect
		connect = Button(master=frame, text='Connect', font=Settings.font_small, command=self.__connect_to_db__)
		connect.grid(row=5, column=1, sticky=E)

	def __connect_to_db__(self):
		# check if all the fields are filled in
		username = self.__username_field.get()
		password = self.__password_field.get()
		port = self.__port_field.get()
		host = self.__host_field.get()
		database = self.__database_field.get()

		


root = Tk()

connect_db = ConnectDbWindow(root)

if __name__ == '__main__':
	root.mainloop()