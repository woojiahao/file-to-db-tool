from tkinter import *
from db_tool import DatabaseTool

class ConvertSetupWindow(Frame):
	def __init__(self, master: Tk, db_tool, DatabaseTool, file_name: str):
		super().__init__(master=master)
		self.__master = master
		self.__tool = db_tool
		self.__config__()

	def __config__(self):
		pass