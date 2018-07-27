from tkinter import *
from tkinter.simpledialog import Dialog

from tool.settings import Settings


class ConnectionStringPopup(Dialog):
	def body(self, master):
		Label(master=master,
			  text='Connection String:',
			  font=Settings.font_small) \
			.grid(row=0, sticky='W',
				  padx=Settings.padding_x,
				  pady=(Settings.padding_y / 2))

		self.__connection_string_str = StringVar()
		self.__connection_string_field = Entry(master=master,
											   textvariable=self.__connection_string_str,
											   font=Settings.font_small)
		self.__connection_string_field.grid(row=1,
											padx=Settings.padding_x)

		return self.__connection_string_field

	def apply(self):
		self.conn_str = self.__connection_string_field.get()
