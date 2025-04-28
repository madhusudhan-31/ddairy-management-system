import mysql.connector
from customtkinter import *
from tkinter import messagebox
from dotenv import load_dotenv
import os
from db_password_prompt import get_password

# ---------------------- Load Environment Variables ----------------------
# Load environment variables from the .env file


import json



# ---------------------- Connect to Database ----------------------
def connect_database():
    global cursor
    global conn
    try:
        # Load the configuration from the JSON file
        with open("db_config.json") as config_file:
            db_config = json.load(config_file)
        db_password = get_password()

        # Establish connection to MySQL
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_password
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