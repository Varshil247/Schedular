import pyodbc
import MErrorPopup as popup

#!########################################################################
try:
    #con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\258488\OneDrive - Loughborough College\Computer Science\2. NEA CODE\Schedular_py\SCHEDULAR APP\schedularAppDatabase.accdb;'
    con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Varshil Patel\OneDrive - Loughborough College\Computer Science\2. NEA CODE\Schedular_py\SCHEDULAR APP\schedularAppDatabase.accdb;'
    conn = pyodbc.connect(con_string)
    print('Connected to Database')

    cur = conn.cursor()

except pyodbc.Error as e: 
    print('Error in Connection', e)
    popup.popup(message='Error in Connection')


