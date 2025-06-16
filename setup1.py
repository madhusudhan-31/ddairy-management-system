import os
import subprocess
import mysql.connector
from getpass import getpass

# Step 1: Install required Python packages
print("Installing required packages...")
subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

# Step 2: Ask for MySQL root password
print("Connecting to MySQL...")
mysql_password = getpass("Enter your MySQL root password: ")

# Step 3: Check if the database exists
try:
    conn = mysql.connector.connect(host="localhost", user="root", password=mysql_password)
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    dbs = [db[0] for db in cursor.fetchall()]
    
    if "member_data" not in dbs:
        print("Database not found. Importing from member_data.sql...")
        os.system(f'mysql -u root -p{mysql_password} < member_data.sql')
    else:
        print("✅ Database 'member_data' already exists. No need to import.")
    
    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print("❌ MySQL Connection Failed:", err) 