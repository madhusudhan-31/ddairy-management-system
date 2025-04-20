from customtkinter import *
from PIL import Image
from tkinter import ttk, messagebox
import database
import subprocess

# ---------- Window Control Flags ----------
is_maximized = True

# ---------- App Functions ----------
def maximize_restore_window():
    global is_maximized
    if is_maximized:
        window.geometry("1100x700+100+100")
        is_maximized = False
    else:
        window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+0+0")
        is_maximized = True

def close_window():
    try:
        window.quit()
        window.destroy()
    except:
        pass

def milk_info():
    try:
        subprocess.Popen(["python", "milk.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open milk window: {e}")

def login():
    try:
        subprocess.Popen(["python", "login.py"])
        window.withdraw()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open login window: {e}")

def restore1():
    tree.delete(*tree.get_children())
    restored_members = database.fetch_restore(idEntry.get())
    for member in restored_members:
        tree.insert('', END, values=member)

def delete_all():
    result = messagebox.askyesno("Confirm", "Are you sure you want to delete all records?")
    if result:
        database.delete_all1()
        treeview_data()

def search_mem():
    if searchEntry.get() == "":
        messagebox.showerror("Error", "Please enter a value to search.")
    elif searchbox.get() == 'Search By':
        messagebox.showerror("Error", "Please select a search option.")
    else:
        searched_data = database.search(searchbox.get(), searchEntry.get())
        tree.delete(*tree.get_children())
        for mem in searched_data:
            tree.insert('', END, values=mem)

def delete_mem():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showerror('Error', 'Select data to delete')
    else:
        for item in selected_items:
            item_id = tree.item(item)['values'][0]
            database.delete(item_id)
        treeview_data()
        clear()
        messagebox.showinfo("Success", "Selected data deleted successfully")

def mem_update():
    item = tree.selection()
    if not item:
        messagebox.showerror("Error", "Select data to update")
    else:
        database.update(
            idEntry.get(),
            nameEntry.get(),
            phnoEntry.get(),
            gender.get(),
            place.get()
        )
        treeview_data()
        clear()
        messagebox.showinfo("Success", "Data updated successfully")

def selection(event):
    selected_item = tree.selection()
    if selected_item:
        row = tree.item(selected_item[0])['values']
        clear()
        idEntry.insert(0, row[0])
        nameEntry.insert(0, row[1])
        phnoEntry.insert(0, row[2])
        gender.set(row[3])
        place.set(row[4])

def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    idEntry.delete(0, END)
    nameEntry.delete(0, END)
    phnoEntry.delete(0, END)
    gender.set("Select Gender")
    place.set("Select Place")

def treeview_data():
    member = database.fetch_mem()
    member.sort(key=lambda x: x[0])
    tree.delete(*tree.get_children())
    for mem in member:
        tree.insert('', END, values=mem)

def add_member():
    if idEntry.get() == "" or phnoEntry.get() == "" or nameEntry.get() == "":
        messagebox.showerror('Error', 'All fields should be filled')
    mobile = phnoEntry.get()
    if not mobile.isdigit() or len(mobile) != 10:
        messagebox.showerror("Error", "Phone number must be 10 digits")
    elif database.id_exists(idEntry.get()):
        messagebox.showerror('Error', "ID already exists")
    else:
        database.insert(
            idEntry.get(),
            nameEntry.get(),
            phnoEntry.get(),
            gender.get(),
            place.get()
        )
        treeview_data()
        messagebox.showinfo("Success", "Data added successfully")
        clear()

def minimize_window():
    window.update_idletasks()
    window.overrideredirect(False)
    window.iconify()

def toggle_max_restore():
    global is_maximized
    if is_maximized:
        window.geometry("1200x700+100+100")
        is_maximized = False
    else:
        window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+0+0")
        is_maximized = True

def select_all_rows():
    for item in tree.get_children():
        tree.selection_add(item)

# ---------- Main Window ----------
set_appearance_mode("light")
window = CTk()
window.title("Member Record")
window.overrideredirect(False)
window.geometry("1400x800")
window.protocol("WM_DELETE_WINDOW", close_window)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

# ---------- Top Header Image ----------
header_img = CTkImage(Image.open("mem1.jpeg"), size=(1410, 200))
CTkLabel(window, image=header_img, text="").grid(row=0, column=0, columnspan=2, sticky="nsew")

# ---------- Main Frame ----------
main_frame = CTkFrame(window, fg_color="#102542")
main_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

leftFrame = CTkFrame(main_frame, fg_color="#102542")
leftFrame.grid(row=0, column=0, padx=100, pady=25, sticky="n")

# rightFrame = CTkFrame(main_frame, fg_color="#102542")
# rightFrame.grid(row=0, column=1, padx=100, pady=30, sticky="n")
rightFrame = CTkFrame(main_frame, corner_radius=15,  border_width=1, fg_color="#102542")
rightFrame.grid(row=0, column=1, sticky="nsew", padx=350, pady=10)

# ---------- Left Inputs ----------
def make_label_entry(frame, text, row):
    label = CTkLabel(frame, text=text, font=('Arial', 18, 'bold'))
    label.grid(row=row, column=0, padx=20, pady=10, sticky='w')
    entry = CTkEntry(frame, font=('Arial', 15), width=160, fg_color='white', text_color="black")
    entry.grid(row=row, column=1, padx=5)
    return entry

idEntry = make_label_entry(leftFrame, "ID", 0)
nameEntry = make_label_entry(leftFrame, "Name", 1)
phnoEntry = make_label_entry(leftFrame, "Phone", 2)

CTkLabel(leftFrame, text='Gender', font=('Arial', 18, 'bold')).grid(row=3, column=0, padx=20, pady=10, sticky='w')
gender = CTkComboBox(leftFrame, values=['Select Gender', 'Male', 'Female'], width=160, fg_color='white', text_color="black")
gender.set("Select Gender")
gender.grid(row=3, column=1)

CTkLabel(leftFrame, text='Place', font=('Arial', 18, 'bold')).grid(row=4, column=0, padx=20, pady=10, sticky='w')
place = CTkComboBox(leftFrame, values=['Select Place', 'Huanasekatte', 'Jpalya', 'Mhatti', 'Pura'], width=160, fg_color='white', text_color="black")
place.set("Select Place")
place.grid(row=4, column=1)

# ---------- Right Search + Treeview ----------
searchbox = CTkComboBox(rightFrame, values=['Search By', 'ID', 'Phone', 'Name', 'Place', 'Gender'], width=100, fg_color='white', text_color="black")
searchbox.set("Search By")
searchbox.grid(row=0, column=0, pady=5, padx=5)

searchEntry = CTkEntry(rightFrame, fg_color='white', text_color="black", width=100)
searchEntry.grid(row=0, column=1, pady=5, padx=5)

CTkButton(rightFrame, text="Search", width=100, command=search_mem).grid(row=0, column=2, pady=5, padx=5)
CTkButton(rightFrame, text="Show All", width=100, command=treeview_data).grid(row=0, column=3, pady=5, padx=5)
CTkButton(rightFrame, text="Select All", width=100, command=select_all_rows).grid(row=0, column=4, pady=5, padx=5)

tree = ttk.Treeview(rightFrame, height=13)
tree.grid(row=1, column=0, columnspan=5, pady=10)
tree['columns'] = ('Id', 'Name', 'Phone', 'Gender', 'Place')
tree.config(show="headings")

for col in tree['columns']:
    tree.heading(col, text=col)
    tree.column(col, width=130)
tree.column("Id", width=100)
tree.column("Gender", width=150)
tree.column("Place", width=150)

scrollbar = ttk.Scrollbar(rightFrame, orient=VERTICAL, command=tree.yview)
scrollbar.grid(row=1, column=5, sticky='ns')
tree.configure(yscrollcommand=scrollbar.set)

style = ttk.Style()
style.configure("Treeview", font=('Arial', 14), rowheight=30, background="#223344", foreground="white", fieldbackground="#223344")

# ---------- Bottom Buttons ----------
buttonFrame = CTkFrame(window, fg_color="#102542")
buttonFrame.grid(row=2, column=0, pady=10)

btn_style = {
    "font": ('Arial', 15, 'bold'),
    "width": 160,
    "text_color": "black",
    "fg_color": "white"
}

CTkButton(buttonFrame, text="Milk Info", command=milk_info, **btn_style).grid(row=0, column=0, padx=5, pady=10)
CTkButton(buttonFrame, text="Add Member", command=add_member, **btn_style).grid(row=0, column=1, padx=5)
CTkButton(buttonFrame, text="Update Member", command=mem_update, **btn_style).grid(row=0, column=2, padx=5)
CTkButton(buttonFrame, text="Delete Member", command=delete_mem, **btn_style).grid(row=0, column=3, padx=5)
CTkButton(buttonFrame, text="Delete All", command=delete_all, **btn_style).grid(row=0, column=4, padx=5)
CTkButton(buttonFrame, text="Back to Login", command=login, **btn_style).grid(row=0, column=5, padx=5)
CTkButton(buttonFrame, text="Restore", command=restore1, **btn_style).grid(row=0, column=6, padx=5)

# ---------- Final Setup ----------
treeview_data()
window.bind("<ButtonRelease>", selection)
window.mainloop()
