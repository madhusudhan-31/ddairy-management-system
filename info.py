from customtkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime

# ------------------- Database Function -------------------
def fetch_by_id_name_and_date(id, name, selected_date):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="madhu@123",
            database="member_data"
        )
        cur = con.cursor()
        query = """
            SELECT * FROM history_rec
            WHERE id = %s AND name = %s AND date <= %s
        """
        cur.execute(query, (id, name, selected_date))
        data = cur.fetchall()
        con.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

# ------------------- Search Button Function -------------------
def search_records():
    id_ = idEntry.get().strip()
    name_ = nameEntry.get().strip()
    selected_date = cal.get_date()

    if not id_ or not name_:
        messagebox.showwarning("Input Required", "Please enter both ID and Name.")
        return

    formatted_date = selected_date.strftime('%Y-%m-%d')
    records = fetch_by_id_name_and_date(id_, name_, formatted_date)
    
    tree.delete(*tree.get_children())

    if records:
        for row in records:
            tree.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    else:
        messagebox.showinfo("No Records", "No milk data found for this ID, Name, and Date.")

# ------------------- Exit Function -------------------
def exit_app():
    root.destroy()

# ------------------- UI Setup -------------------
root = CTk()
root.title("Milk Update History Viewer")
root.geometry("1050x600")
set_default_color_theme("blue")

main_frame = CTkFrame(root, corner_radius=12)
main_frame.pack(pady=30, padx=30, fill='both', expand=True)

# ----------- Inputs ----------- 
CTkLabel(main_frame, text="Enter Member ID:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
idEntry = CTkEntry(main_frame, width=200)
idEntry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

CTkLabel(main_frame, text="Enter Member Name:", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
nameEntry = CTkEntry(main_frame, width=200)
nameEntry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

CTkLabel(main_frame, text="Select Date:", font=("Arial", 16)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
cal = DateEntry(main_frame, width=18, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
cal.grid(row=2, column=1, padx=10, pady=10, sticky='w')

search_btn = CTkButton(main_frame, text="Search", command=search_records)
search_btn.grid(row=3, column=0, pady=20)

exit_btn = CTkButton(main_frame, text="Exit", command=exit_app)
exit_btn.grid(row=3, column=2, pady=20)

# ----------- Treeview ----------- 
columns = ("ID", "Name", "Quantity", "Type", "Amount", "Email", "Updated At")
tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor='center')

tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

main_frame.grid_rowconfigure(4, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

root.mainloop()
