from tkinter import *

from tool.convert_setup_window import ConvertSetupWindow
from tool.db_tool import DatabaseTool
from tool.file_selection_window import FileSelectionWindow


def launch_file_selection(root: Tk, tool: DatabaseTool):
	root.destroy()
	FileSelectionWindow(Tk(), tool)


def launch_setup(root: Tk, tool: DatabaseTool, filename: str,
				 skiprows: int, delimiter: str, missing_values: list,
				 fill_value: str):
	root.destroy()
	ConvertSetupWindow(Tk(), tool, filename, skiprows, delimiter, missing_values, fill_value)
