from customtkinter import *
import mysql.connector
from PIL import Image
from tkinter import ttk, messagebox
import database1 
import subprocess
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from tkcalendar import DateEntry

# -------------------- EMAIL FUNCTION --------------------
def send_email(to_email, subject, body):
    sender_email = "madhusudhangowdahg31@gmail.com"
    sender_password = "fejs sppy xdew v izh"  # App password from Gmail

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        messagebox.showinfo("Email Sent", f"Successfully sent to {to_email}")
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send email: {e}")

def send_email_from_form():
    to_email = emailEntry.get().strip()
    if "@" not in to_email or "." not in to_email:
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    try:
        float_quality = float(qualityEntry.get())
        float_prize = float(prize.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Milk Quality and Amount must be numbers.")
        return

    subject = "Milk Entry Confirmation"
    body = f"""
Hello,

The following milk entry has been recorded:

🆔 ID: {idEntry.get()}
👤 Name: {nameEntry.get()}
🥛 Milk Quantity: {float_quality:.2f} L
🐄 Type: {Type.get()}
💰 Amount: ₹{float_prize:.2f}
📅 Date: {dateEntry.get()}

Thank you.
"""
    send_email(to_email, subject, body)

# -------------------- MAIN FUNCTIONAL HANDLERS --------------------
def clear_fields(deselect=False):
    if deselect:
        tree.selection_remove(tree.focus())
    idEntry.delete(0, END)
    nameEntry.delete(0, END)
    qualityEntry.delete(0, END)
    Type.set("Select type")
    prize.set("Select")
    emailEntry.delete(0, END)
    dateEntry.set_date(datetime.today())

def refresh_table(data):
    tree.delete(*tree.get_children())
    for item in data:
        tree.insert('', END, values=item)

def treeview_data():
    refresh_table(database1.fetch_mem())

def treeview_data1():
    refresh_table(database1.rank())

def submit():
    if not all([idEntry.get(), nameEntry.get(), emailEntry.get()]):
        messagebox.showerror("Missing Fields", "Please fill in all required fields.")
        return

    if "@" not in emailEntry.get() or "." not in emailEntry.get():
        messagebox.showerror("Invalid Email", "Enter a valid email address.")
        return

    # ✅ Check if id & name exist in both milk1 and data1
    if not database1.id_exists(idEntry.get(), nameEntry.get()):
        messagebox.showerror("ID/Name Error", "ID and Name must be registerd.")
        return
    if database1.id_exists1(idEntry.get()):
        messagebox.showerror('Error', "ID already exists")
        return

    try:
        date_obj = dateEntry.get_date()
        formatted_date = date_obj.strftime("%Y-%m-%d")
        database1.insert(
            idEntry.get(), nameEntry.get(), float(qualityEntry.get()), Type.get(),
            float(prize.get()), emailEntry.get(), formatted_date
        )
        database1.insert1(
            idEntry.get(), nameEntry.get(), float(qualityEntry.get()), Type.get(),
            float(prize.get()), emailEntry.get(), formatted_date
        )
        treeview_data()
        messagebox.showinfo("Success", "Milk entry added.")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))


def mem_update():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Selection Error", "Select a row to update.")
        return

    try:
        formatted_date = dateEntry.get_date().strftime("%Y-%m-%d")
        database1.update(
            idEntry.get(), nameEntry.get(), float(qualityEntry.get()), Type.get(),
            float(prize.get()), emailEntry.get(), formatted_date
        )
        treeview_data()
        messagebox.showinfo("Success", "Data updated.")
        clear_fields(True)
    except Exception as e:
        messagebox.showerror("Update Error", str(e))

def delete_mem():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Selection Error", "Select at least one row to delete.")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete selected records?")
    if confirm:
        for item in selected:
            selected_id = tree.item(item)['values'][0]
            database1.delete(selected_id)
        treeview_data()
        clear_fields(True)
        messagebox.showinfo("Deleted", "Selected records deleted.")

def selection(event):
    selected = tree.selection()
    if selected:
        # Optional: print all selected IDs
        print("Selected IDs:", [tree.item(item)['values'][0] for item in selected])

        # Fill form with the first selected row
        row = tree.item(selected[0])['values']
        clear_fields()
        idEntry.insert(0, row[0])
        nameEntry.insert(0, row[1])
        qualityEntry.insert(0, row[2])
        Type.set(row[3])
        prize.set(str(row[4]))
        emailEntry.insert(0, row[5])
        try:
            date_obj = datetime.strptime(row[6], "%Y-%m-%d").date()
            dateEntry.set_date(date_obj)
        except Exception as e:
            messagebox.showerror("Date Error", f"Invalid date: {e}")

def back_to_mem():
    subprocess.Popen(["python", "mem.py"])
    milkwindow.withdraw()

# -------------------- UI SETUP --------------------
milkwindow = CTk()
milkwindow.title("Milk Entry Portal")
milkwindow.geometry("1400x800")
milkwindow.configure(fg_color="#F4F8FB")
set_appearance_mode("light")
set_default_color_theme("blue")

milkwindow.grid_rowconfigure(1, weight=1)
milkwindow.grid_columnconfigure(0, weight=1)
milkwindow.grid_columnconfigure(1, weight=2)

header_img = CTkImage(Image.open("Milk-milk-35325289-600-450.jpg"), size=(1400, 180))
CTkLabel(milkwindow, image=header_img, text="").grid(row=0, column=0, columnspan=2, sticky="nsew")

leftFrame = CTkFrame(milkwindow, corner_radius=15, border_width=1, border_color="#cccccc", fg_color="#ffffff")
leftFrame.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
leftFrame.columnconfigure((0, 1), weight=1)

def make_label_entry(frame, label_text, row):
    CTkLabel(frame, text=label_text, font=('Arial', 17, 'bold'), text_color="#333333").grid(row=row, column=0, padx=20, pady=10, sticky='w')
    entry = CTkEntry(frame, font=('Arial', 15), width=200, height=40, fg_color='#F0F0F0')
    entry.grid(row=row, column=1, padx=10)
    return entry

idEntry = make_label_entry(leftFrame, "ID", 0)
nameEntry = make_label_entry(leftFrame, "Name", 1)
qualityEntry = make_label_entry(leftFrame, "Milk Quality (L)", 2)

CTkLabel(leftFrame, text="Type", font=('Arial', 17, 'bold')).grid(row=3, column=0, padx=20, pady=10, sticky='w')
Type = CTkComboBox(leftFrame, values=["Select type", "Cow", "Buffalo"], width=200)
Type.set("Select type")
Type.grid(row=3, column=1, padx=10)

CTkLabel(leftFrame, text="Amount", font=('Arial', 17, 'bold')).grid(row=4, column=0, padx=20, pady=10, sticky='w')
prize = CTkComboBox(leftFrame, values=["Select", "40", "45"], width=200)
prize.set("Select")
prize.grid(row=4, column=1, padx=10)

emailEntry = make_label_entry(leftFrame, "Email", 5)

CTkLabel(leftFrame, text="Date", font=('Arial', 17, 'bold')).grid(row=6, column=0, padx=20, pady=10, sticky='w')
dateEntry = DateEntry(leftFrame, width=18, font=('Arial', 15), fg_color="#ffffff")
dateEntry.set_date(datetime.today())
dateEntry.grid(row=6, column=1, padx=10)

CTkButton(leftFrame, text="Submit", command=submit, font=('Arial', 15, 'bold'), width=150).grid(row=7, column=0, pady=10)
CTkButton(leftFrame, text="Update", command=mem_update, font=('Arial', 15, 'bold'), width=150, fg_color="orange").grid(row=7, column=1, pady=10)
CTkButton(leftFrame, text="Delete", command=delete_mem, font=('Arial', 15, 'bold'), width=150, fg_color="red").grid(row=8, column=0, pady=10)
CTkButton(leftFrame, text="Rank", command=treeview_data1, font=('Arial', 15, 'bold'), width=150).grid(row=8, column=1, pady=10)
CTkButton(leftFrame, text="Send Email", command=send_email_from_form, font=('Arial', 15, 'bold'), width=320, fg_color="green").grid(row=9, column=0, columnspan=2, pady=10)
CTkButton(leftFrame, text="Back to Member Page", command=back_to_mem, font=('Arial', 15, 'bold'), width=320, fg_color="#666666").grid(row=10, column=0, columnspan=2, pady=10)

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
tree = ttk.Treeview(RightFrame, columns=columns, show="headings", selectmode="extended")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor='center', width=130)

tree.grid(row=0, column=0, sticky="nsew")
scrollbar = ttk.Scrollbar(RightFrame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")
tree.bind("<<TreeviewSelect>>", selection)

treeview_data()
milkwindow.mainloop()
