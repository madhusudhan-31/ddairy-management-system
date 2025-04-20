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
        cursor.execute("CREATE DATABASE IF NOT EXISTS member_data")
        cursor.execute("USE member_data")

        # Create the data1 table (original member data)
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS data1 (
                ID VARCHAR(20) PRIMARY KEY,
                Name VARCHAR(50),
                Phone VARCHAR(50),
                Gender VARCHAR(50),
                Place VARCHAR(50)
            )
        ''')

        # Create the restore table to hold deleted members
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS member_restore (
                ID VARCHAR(20) PRIMARY KEY,
                Name VARCHAR(50),
                Phone VARCHAR(50),
                Gender VARCHAR(50),
                Place VARCHAR(50),
                DeletedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

def insert(id, name, phno, gender, place):
    if id_exists(id):
        messagebox.showerror("Error", f"ID {id} already exists in the database.")
        return
    
    cursor.execute('INSERT INTO data1 VALUES(%s,%s,%s,%s,%s)', (id, name, phno, gender, place))
    conn.commit()

def id_exists(id):
    cursor.execute("SELECT COUNT(*) FROM data1 WHERE ID=%s", (id,))
    result = cursor.fetchone()
    return result[0] > 0

def fetch_mem():
    cursor.execute("SELECT * FROM data1")
    result = cursor.fetchall()
    return result

def fetch_restore(id):
    cursor.execute("SELECT * FROM data1 WHERE ID=%s", (id,))
    record = cursor.fetchall()
    if record:
        cursor.execute("INSERT INTO member_restore (ID, Name, Phone, Gender, Place) VALUES (%s, %s, %s, %s, %s)", 
                           (record[0], record[1], record[2], record[3], record[4]))
        conn.commit()
    cursor.execute("SELECT * FROM member_restore")
    result = cursor.fetchall()
    return result

def update(id, new_name, new_phon, new_gender, new_palce):
    cursor.execute("UPDATE data1 SET Name=%s, Phone=%s, Gender=%s, Place=%s WHERE ID=%s", 
                   (new_name, new_phon, new_gender, new_palce, id))
    conn.commit()
    
   

    messagebox.showinfo("Success", f"Member with ID {id} updated successfully.")

def delete(id):
    # Check if the member exists in data1
    cursor.execute("SELECT * FROM data1 WHERE ID=%s", (id,))
    record = cursor.fetchone()

    if record:
        # Before deleting, check if the record already exists in the restore table
        cursor.execute("SELECT COUNT(*) FROM member_restore WHERE ID=%s", (id,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Insert into member_restore if not already there
            cursor.execute("INSERT INTO member_restore (ID, Name, Phone, Gender, Place) VALUES (%s, %s, %s, %s, %s)", 
                           (record[0], record[1], record[2], record[3], record[4]))
            conn.commit()

        # Delete the record from the original table
        cursor.execute("DELETE FROM data1 WHERE ID=%s", (id,))
        conn.commit()

        messagebox.showinfo("Success", f"Member with ID {id} deleted and moved to restore.")
    else:
        messagebox.showerror("Error", "No member found with this ID.")

def restore(id):
    # Restore a deleted member from the restore table back to the original table
    cursor.execute("SELECT * FROM member_restore WHERE ID=%s", (id,))
    record = cursor.fetchone()
    if record:
        cursor.execute("INSERT INTO data1 (ID, Name, Phone, Gender, Place) VALUES (%s, %s, %s, %s, %s)", 
                       (record[0], record[1], record[2], record[3], record[4]))
        conn.commit()

        # Now delete the record from the restore table
        cursor.execute("DELETE FROM member_restore WHERE ID=%s", (id,))
        conn.commit()
        messagebox.showinfo("Success", f"Member with ID {id} restored successfully.")
    else:
        messagebox.showerror("Error", "No member found in restore table with this ID.")

def search(option, value):
    allowed_columns = ['ID', 'Name', 'Phone', 'Gender', 'Place']
    if option not in allowed_columns:
        return []

    query = f"SELECT * FROM data1 WHERE {option} LIKE %s"
    cursor.execute(query, (f"%{value}%",))
    return cursor.fetchall()

def delete_all1():
    cursor.execute("TRUNCATE TABLE data1")
    conn.commit()

# Connect to the database
connect_database()
