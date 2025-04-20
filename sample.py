from customtkinter import *
import mysql.connector
from PIL import Image
from tkinter import ttk, messagebox
import database1 as database1
import subprocess
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from tkcalendar import DateEntry

# ------------ EMAIL FUNCTION ------------
def send_email(to_email, subject, body):
    sender_email = "madhusudhangowdahg31@gmail.com"
    sender_password = "fejs sppy xdew vizh"  # Gmail app password

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.set_debuglevel(1)
            server.login(sender_email, sender_password)
            server.send_message(msg)
        messagebox.showinfo("Email", f"Email sent successfully to {to_email}!")
    except Exception as e:
        messagebox.showerror("Email Failed", str(e))

def send_email_from_form():
    recipient_email = emailEntry.get().strip()
    if not recipient_email or "@" not in recipient_email or "." not in recipient_email:
        messagebox.showerror("Error", "Enter a valid email address")
        return

    if not nameEntry.get() or not qualityEntry.get() or not prize.get().isdigit():
        messagebox.showerror("Error", "Please ensure Name, Quality and Price are filled correctly.")
        return

    subject = "Milk Entry Confirmation"
    body = f"""
Hello,

The following milk entry has been recorded:

🆔 ID: {idEntry.get()}
👤 Name: {nameEntry.get()}
🥛 Milk Quality: {qualityEntry.get()} Litres
🐄 Type: {Type.get()}
💰 Amount: ₹{prize.get()}
📅 Date: {dateEntry.get()}

Thank you.
"""
    send_email(recipient_email, subject, body)

# ------------ DB + HANDLER FUNCTIONS ------------
def close_window():
    milkwindow.destroy()

def mem():
    subprocess.Popen(["python", "mem.py"])

def rank():
    treeview_data1()

def mem_update():
    item = tree.selection()
    if not item:
        messagebox.showerror("Error", "Select data to update")
        return

    if (not idEntry.get() or not nameEntry.get() or not qualityEntry.get().isdigit() 
        or Type.get() == "Select type" or not prize.get().isdigit()):
        messagebox.showerror("Error", "All fields must be properly filled before updating.")
        return

    milk_date = dateEntry.get()
    try:
        database1.update(idEntry.get(), nameEntry.get(), int(qualityEntry.get()), Type.get(),
                         int(prize.get()), emailEntry.get(), milk_date)
        treeview_data()
        clear()
        messagebox.showinfo("Success", "Data updated successfully")
    except Exception as e:
        messagebox.showerror("Error during update", str(e))

def selection(event):
    selected_item = tree.selection()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        idEntry.insert(0, row[0])
        nameEntry.insert(0, row[1])
        qualityEntry.insert(0, row[2])
        Type.set(row[3])
        prize.set(str(row[4]))
        emailEntry.insert(0, row[5])
        dateEntry.set_date(row[6])

def delete_mem():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select data to delete')
        return
    selected_id = tree.item(selected_item)['values'][0]
    confirm = messagebox.askyesno("Confirm", f"Delete entry with ID: {selected_id}?")
    if confirm:
        database1.delete(selected_id)
        treeview_data()
        clear(True)
        messagebox.showinfo("Success", "Data deleted successfully")

def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    idEntry.delete(0, END)
    nameEntry.delete(0, END)
    emailEntry.delete(0, END)
    qualityEntry.delete(0, END)
    Type.set("Select type")
    prize.set("Select")
    dateEntry.set_date(datetime.today())

def treeview_data1():
    members = database1.rank()
    tree.delete(*tree.get_children())
    for mem in members:
        tree.insert('', END, values=mem)

def treeview_data():
    members = database1.fetch_mem()
    tree.delete(*tree.get_children())
    for mem in members:
        tree.insert('', END, values=mem)

def submit():
    if idEntry.get() == "" or nameEntry.get() == '' or emailEntry.get() == '':
        messagebox.showerror("Error", "All fields should be filled")
        return

    if "@" not in emailEntry.get() or "." not in emailEntry.get():
        messagebox.showerror("Error", "Enter a valid email")
        return

    if database1.id_exists(idEntry.get()):
        messagebox.showerror('Error', "ID already exists")
        return

    database1.insert(idEntry.get(), nameEntry.get(), qualityEntry.get(), Type.get(),
                     prize.get(), emailEntry.get(), dateEntry.get())
    treeview_data()
    messagebox.showinfo("Success", "Data has been added successfully")
    clear()

# ------------ MAIN WINDOW SETUP ------------
milkwindow = CTk()
milkwindow.title("Milk Details")
milkwindow.geometry("1400x800")
milkwindow.configure(fg_color="#F4F8FB")

milkwindow.grid_rowconfigure(1, weight=1)
milkwindow.grid_columnconfigure(0, weight=1)
milkwindow.grid_columnconfigure(1, weight=2)

set_appearance_mode("light")
set_default_color_theme("blue")

# ------------ HEADER IMAGE ------------
header_img = CTkImage(Image.open("Milk-milk-35325289-600-450.jpg"), size=(1400, 180))
header_label = CTkLabel(milkwindow, image=header_img, text="")
header_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

# ------------ LEFT PANEL ------------
leftFrame = CTkFrame(milkwindow, corner_radius=15, border_width=1, border_color="#cccccc", fg_color="#ffffff")
leftFrame.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
leftFrame.columnconfigure((0, 1), weight=1)

def make_label_entry(frame, text, row):
    label = CTkLabel(frame, text=text, font=('Arial', 17, 'bold'), text_color="#333333")
    label.grid(row=row, column=0, padx=20, pady=10, sticky='w')
    entry = CTkEntry(frame, font=('Arial', 15), width=200, height=40, fg_color='#F0F0F0')
    entry.grid(row=row, column=1, padx=10)
    return entry

idEntry = make_label_entry(leftFrame, "ID", 0)
nameEntry = make_label_entry(leftFrame, "Name", 1)
qualityEntry = make_label_entry(leftFrame, "Milk Quality (L)", 2)

CTkLabel(leftFrame, text="Type", font=('Arial', 17, 'bold'), text_color="#333333").grid(row=3, column=0, padx=20, pady=10, sticky='w')
Type = CTkComboBox(leftFrame, values=["Select type", "Cow", "Buffalo"], width=200)
Type.set("Select type")
Type.grid(row=3, column=1, padx=10)

CTkLabel(leftFrame, text="Amount", font=('Arial', 17, 'bold'), text_color="#333333").grid(row=4, column=0, padx=20, pady=10, sticky='w')
prize = CTkComboBox(leftFrame, values=["Select", "40", "45"], width=200)
prize.set("Select")
prize.grid(row=4, column=1, padx=10)

emailEntry = make_label_entry(leftFrame, "Email", 5)

CTkLabel(leftFrame, text="Date", font=('Arial', 17, 'bold'), text_color="#333333").grid(row=6, column=0, padx=20, pady=10, sticky='w')
dateEntry = DateEntry(leftFrame, width=18, font=('Arial', 15), fg_color="#ffffff")
dateEntry.set_date(datetime.today())
dateEntry.grid(row=6, column=1, padx=10)

CTkButton(leftFrame, text="Submit", font=('Arial', 15, 'bold'), width=150, command=submit).grid(row=7, column=0, pady=10)
CTkButton(leftFrame, text="Update", font=('Arial', 15, 'bold'), width=150, fg_color="orange", command=mem_update).grid(row=7, column=1, pady=10)
CTkButton(leftFrame, text="Delete", font=('Arial', 15, 'bold'), width=150, fg_color="red", command=delete_mem).grid(row=8, column=0, pady=10)
CTkButton(leftFrame, text="Rank", font=('Arial', 15, 'bold'), width=150, command=rank).grid(row=8, column=1, pady=10)
CTkButton(leftFrame, text="Send Email", font=('Arial', 15, 'bold'), width=320, fg_color="green", command=send_email_from_form).grid(row=9, column=0, columnspan=2, pady=10)
CTkButton(leftFrame, text="Back to Member Page", font=('Arial', 15, 'bold'), width=320, fg_color="#666666", command=mem).grid(row=10, column=0, columnspan=2, pady=10)

# ------------ RIGHT PANEL (TABLE) ------------
RightFrame = CTkFrame(milkwindow, corner_radius=15, border_color="#cccccc", border_width=1, fg_color="#ffffff")
RightFrame.grid(row=1, column=1, sticky="nsew", padx=(0, 30), pady=30)
RightFrame.grid_rowconfigure(0, weight=1)
RightFrame.grid_columnconfigure(0, weight=1)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=('Arial', 12), rowheight=32, background="#ffffff", fieldbackground="#ffffff", foreground="black")
style.configure("Treeview.Heading", font=('Arial', 14, 'bold'), background="#1E90FF", foreground="white")
style.map("Treeview", background=[('selected', '#B0E0E6')])

columns = ("ID", "Name", "Quality", "Type", "Amount", "Email", "Date")
tree = ttk.Treeview(RightFrame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor='center', width=130)

tree.grid(row=0, column=0, sticky="nsew")
scrollbar = ttk.Scrollbar(RightFrame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")
tree.bind("<<TreeviewSelect>>", selection)

# Load initial data
treeview_data()
milkwindow.mainloop()
  
  def selection(event):
    selected_item = tree.selection()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        idEntry.insert(0, row[0])
        nameEntry.insert(0, row[1])
        qualityEntry.insert(0, row[2])
        Type.set(row[3])
        prize.set(str(row[4]))
        emailEntry.insert(0, row[5])
        dateEntry.set_date(row[6])