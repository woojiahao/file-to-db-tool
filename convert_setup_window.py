from tkinter import *
from db_tool import DatabaseTool

class ConvertSetupWindow(Frame):
	def __init__(self, master: Tk, db_tool: DatabaseTool, filename: str, skiprows: int, delimiter: str):
		super().__init__(master=master)
		self.__master = master
		self.__tool = db_tool
		self.__filename = filename
		self.__config__()

	def __config__(self):
		pass