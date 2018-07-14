from tkinter import Frame, Tk

from db_tool import DatabaseTool

class MainWindow(Frame):
	def __init__(self, master: Tk, db_tool: DatabaseTool):
		super().__init__(master=master)
		self.__tool = db_tool
