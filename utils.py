from tkinter import *
from tkinter import messagebox

from file_selection_window import FileSelectionWindow
from convert_setup_window import ConvertSetupWindow
from db_tool import DatabaseTool

def launch_file_selection(root: Tk, tool: DatabaseTool):
	root.destroy()
	FileSelectionWindow(Tk(), tool)

def launch_setup(root: Tk, tool: DatabaseTool, filename: str, skiprows: int, delimiter: str):
	root.destroy()
	ConvertSetupWindow(Tk(), tool, filename, skiprows, delimiter)
