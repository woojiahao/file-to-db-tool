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

		username = Label(master=frame, text='Username:', font=Settings.font_small)
		password = Label(master=frame, text='Password:', font=Settings.font_small)
		port = Label(master=frame, text='Port:', font=Settings.font_small)
		host = Label(master=frame, text='Host:', font=Settings.font_small)
		database = Label(master=frame, text='Database:', font=Settings.font_small)

		username_field = Entry(master=frame, font=Settings.font_small)
		password_field = Entry(master=frame, font=Settings.font_small)
		port_field = Entry(master=frame, font=Settings.font_small)
		host_field = Entry(master=frame, font=Settings.font_small)
		database_field = Entry(master=frame, font=Settings.font_small)

		username.grid(row=0, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		password.grid(row=1, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		port.grid(row=2, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		host.grid(row=3, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))
		database.grid(row=4, sticky=W, padx=(0, Settings.padding_x), pady=(0, Settings.padding_y))

		username_field.grid(row=0, column=1, pady=(0, Settings.padding_y))
		password_field.grid(row=1, column=1, pady=(0, Settings.padding_y))
		port_field.grid(row=2, column=1, pady=(0, Settings.padding_y))
		host_field.grid(row=3, column=1, pady=(0, Settings.padding_y))
		database_field.grid(row=4, column=1, pady=(0, Settings.padding_y))

	

root = Tk()

connect_db = ConnectDbWindow(root)

if __name__ == '__main__':
	root.mainloop()