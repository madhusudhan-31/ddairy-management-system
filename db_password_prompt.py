import tkinter as tk
import tkinter.simpledialog as simpledialog

def get_password():
    root = tk.Tk()
    root.withdraw()
    password = simpledialog.askstring("Database Login", "Enter MySQL Password:", show='*')
    root.destroy()
    return password
