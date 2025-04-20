import mysql.connector
from customtkinter import *
from tkinter import messagebox
from datetime import datetime

# ---------------------- Connect to Database ----------------------
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
        cursor.execute("USE member_data")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS milk1 (
                id VARCHAR(40) PRIMARY KEY,
                Name VARCHAR(20),
                mail VARCHAR(50),
                Quality INT,
                Type VARCHAR(50),
                AMMOUNT INT,
                date DATE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS update_log (
                id VARCHAR(40),
                Name VARCHAR(20),
                mail VARCHAR(50),
                Quality INT,
                Type VARCHAR(50),
                AMMOUNT INT,
                date DATE,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

# ---------------------- Rate Logic ----------------------
def get_rate(milk_type):
    if milk_type.lower() == "cow":
        return 40
    elif milk_type.lower() == "buffalo":
        return 45
    else:
        return 0

# ---------------------- Ranking ----------------------
def rank():
    cursor.execute("SELECT * FROM milk1 ORDER BY Quality DESC")
    return cursor.fetchall()

# ---------------------- Insert ----------------------
def insert(Id, Name, mail, Quality, Type, AMMOUNT, date):
    cursor.execute(
        "INSERT INTO milk1 (id, Name, mail, Quality, Type, AMMOUNT, date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (Id, Name, mail, Quality, Type, AMMOUNT, date)
    )
    conn.commit()

# ---------------------- Fetch Current Records ----------------------
def fetch_mem():
    cursor.execute("SELECT * FROM milk1")
    return cursor.fetchall()

# ---------------------- Fetch Update Log ----------------------
def fetch_update_log():
    cursor.execute("SELECT * FROM update_log")
    return cursor.fetchall()

# ---------------------- Delete ----------------------
def delete(id):
    cursor.execute("DELETE FROM milk1 WHERE id=%s", (id,))
    conn.commit()

# ---------------------- Update ----------------------
def update(Id, Name, Quality, Type, Ammount, mail, date):
    try:
        # Fetch the previous record
        cursor.execute("SELECT * FROM milk1 WHERE Id = %s", (Id,))
        result = cursor.fetchall()

        if result:
            # Move the current record to the update_log table
            old_record = result[0]
            cursor.execute(
                "INSERT INTO update_log (id, Name, mail, Quality, Type, AMMOUNT, date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                old_record
            )
            conn.commit()

            # Update the milk1 table with new data
            new_amount = int(Quality) * int(Ammount)
            cursor.execute(
                "UPDATE milk1 SET Quality = %s, AMMOUNT = %s, Type = %s, Name = %s, mail = %s, date = %s WHERE Id = %s",
                (Quality, new_amount, Type, Name, mail, date, Id)
            )
            conn.commit()
            print("Update successful")
        else:
            # If the record does not exist, insert a new one
            new_amount = int(Quality) * int(Ammount)
            cursor.execute(
                "INSERT INTO milk1 (Id, Name, mail, Quality, Type, AMMOUNT, date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (Id, Name, mail, Quality, Type, new_amount, date)
            )
            conn.commit()

    except mysql.connector.Error as err:
        print("MySQL Error during update:", err)
    except Exception as e:
        print("Error during update:", e)

# ---------------------- ID Check ----------------------
def id_exists(id):
    cursor.execute("SELECT COUNT(*) FROM milk1 WHERE id=%s", (id,))
    result = cursor.fetchone()
    return result[0] > 0

# ---------------------- Initialize ----------------------
connect_database()
