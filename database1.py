import mysql.connector
from customtkinter import *
from tkinter import messagebox

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

        # Check current schema

        # Alter the columns to FLOAT if needed
        try:
            cursor.execute('ALTER TABLE milk1 MODIFY COLUMN AMMOUNT FLOAT')
            cursor.execute('ALTER TABLE milk1 MODIFY COLUMN Quality FLOAT')
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error updating column types: {err}")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS milk1 (
                id VARCHAR(40),
                Name VARCHAR(20),
                mail VARCHAR(50),
                Quality FLOAT,
                Type VARCHAR(50),
                AMMOUNT FLOAT,
                date DATE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history_rec (
                id VARCHAR(40),
                Name VARCHAR(20),
                mail VARCHAR(50),
                Quality FLOAT,
                Type VARCHAR(50),
                AMMOUNT FLOAT,
                date DATE
            )
        ''')

        cursor.execute("SHOW COLUMNS FROM milk1 LIKE 'date'")
        if cursor.fetchone() is None:
            cursor.execute("ALTER TABLE milk1 ADD COLUMN date DATE")
            conn.commit()

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

# ---------------------- Get Rate ----------------------
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
def insert(Id, Name, Quality, Type, AMMOUNT, mail, date):
    cursor.execute(
        "INSERT INTO milk1 (id, Name, Quality, Type, AMMOUNT, mail, date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (Id, Name, Quality, Type, AMMOUNT, mail, date)
        
    )
    conn.commit()
def insert1(Id, Name, Quality, Type, Ammount, mail, date):
    cursor.execute(
                "INSERT INTO history_rec(Id, Name, mail, Quality, Type, AMMOUNT, date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (Id, Name, mail, Quality, Type, Ammount, date))
    
    conn.commit()

# ---------------------- Fetch ----------------------
def fetch_mem():
    cursor.execute("SELECT * FROM milk1")
    return cursor.fetchall()

# ---------------------- Delete ----------------------
def delete(id):
    cursor.execute("DELETE FROM milk1 WHERE id=%s", (id,))
    conn.commit()

# ---------------------- Update ----------------------
def update(Id, Name, Quality, Type, Ammount, mail, date):
    try:
        cursor.execute("SELECT Quality, AMMOUNT FROM milk1 WHERE Id = %s", (Id,))
        result1 = cursor.fetchall()
        if result1:
            cursor.execute(
                "INSERT INTO history_rec(Id, Name, mail, Quality, Type, AMMOUNT, date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (Id, Name, mail, Quality, Type, Ammount, date))

        cursor.execute("SELECT Quality, AMMOUNT FROM milk1 WHERE Id = %s", (Id,))
        result = cursor.fetchall()  # Process the result before the next query

        if result:
            old_quality, old_amount = result[0]
            new_quality = old_quality + float(Quality)
            new_amount = old_amount + (float(Ammount) * float(Quality))

            cursor.execute(
                "UPDATE milk1 SET Quality = %s, AMMOUNT = %s, Type = %s, Name = %s, mail = %s, date = %s WHERE Id = %s",
                (new_quality, new_amount, Type, Name, mail, date, Id)
            )
        else:
            new_amount = float(Quality) * float(Ammount)
            cursor.execute(
                "INSERT INTO milk1 (Id, Name, mail, Quality, Type, AMMOUNT, date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (Id, Name, mail, Quality, Type, new_amount, date)
            )

        conn.commit()
        print("Update successful")

    except mysql.connector.Error as err:
        print("MySQL Error during update:", err)
    except Exception as e:
        print("Error during update:", e)

# ---------------------- ID Check ----------------------
def id_exists(id,name):
    cursor.execute("SELECT COUNT(*) FROM data1 WHERE id=%s AND name=%s", (id,name))
    result = cursor.fetchone()
    return result[0] > 0
def id_exists1(id):
    cursor.execute("SELECT COUNT(*) FROM milk1 WHERE id=%s ", (id,))
    result = cursor.fetchone()
    return result[0] > 0


# ---------------------- Close Connection ----------------------
def close_connection():
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection closed")

# ---------------------- Initialize ----------------------
connect_database()
