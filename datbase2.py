import mysql.connector
from tkinter import messagebox

def connect_database():
    global cursor
    global conn
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="madhu@123"
        )
        cursor = conn.cursor()
        
        # Create the database
        cursor.execute("USE member_data")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login (
                Name VARCHAR(50),
                Password VARCHAR(50),
                Email VARCHAR(50)
             
            )
        ''')
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")
def insert( name, pasword,mail):
   cursor.execute('INSERT INTO login VALUES(%s,%s,%s)',(name,pasword,mail))
   conn.commit()

connect_database()