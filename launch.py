from tkinter import Tk

from connect_database_window import ConnectDatabaseWindow

root = Tk()
connect_db = ConnectDatabaseWindow(root)

if __name__ == '__main__':
	root.mainloop()