# This file is unique for every computer.

import sqlite3


def connect_sqlite_db():
        conn = sqlite3.connect('C:\Pelle\Dashboard_Python\dashboard_md5.sql3', check_same_thread=False)  # LeanMean
	#conn = sqlite3.connect('G:\PelleHack\Python_Dashboard\dashboard_md5.sql3', check_same_thread=False) # W12

        return conn
