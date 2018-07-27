import json
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


def set_entry_text(entry: Entry, text: str):
	entry.delete(0, END)
	entry.insert(0, text)


def read_configuration_file(file_name: str):
	with open('config/{}'.format(file_name)) as f:
		attrs = json.load(f)
	return attrs


def create_connection_string(username: str, password: str, host: str, port: str, database: str, dialect: str):
	return '{}://{}:{}@{}:{}/{}'.format(dialect, username, password, host, port, database)

def extract_db_from_conn_str(conn_str: str):
	return conn_str[conn_str.rfind('/') + 1 : ]