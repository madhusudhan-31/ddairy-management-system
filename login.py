import mysql.connector
from customtkinter import *
from PIL import Image
from tkinter import messagebox
import subprocess

def login():
    username = usernameEntry.get()
    password = passwordEntry.get()

    if username == '' or password == '':
        messagebox.showerror('Error', "Username and password cannot be empty")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="madhu@123",
            database="member_data"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE name=%s AND pasword=%s", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            messagebox.showinfo("Login Success", f"Welcome {username}!")
            root.withdraw()
            subprocess.Popen(["python", "project/mem.py"])  # ✅ only runs if user is found
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")  # ❌ only shows if no user

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")


def open_register_window():
    try:
        subprocess.Popen(["python", "register.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open registration window: {e}")

def forgot():
    try:
        subprocess.Popen(["python", "forgot.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open registration window: {e}")

def back():
    try:
        subprocess.Popen(["python", "main.py"])
        root.withdraw()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open registration window: {e}")

def submit_on_enter(event):
    login()

def minimize_window():
    root.update_idletasks()
    root.overrideredirect(False)
    root.iconify()

def toggle_max_restore():
    global is_maximized
    if is_maximized:
        root.geometry("1200x700+100+100")
        is_maximized = False
    else:
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        is_maximized = True

def close_window():
    root.destroy()

# ------------------ Window Setup ------------------ #
set_appearance_mode("light")
root = CTk()
root.title("")
root.overrideredirect(False)
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
is_maximized = True

# ------------------ Custom Title Bar ------------------ #
titlebar = CTkFrame(root, height=40, fg_color="#e0f7fa")
titlebar.pack(fill="x", side="top")

CTkLabel(titlebar, text="  ನಂದಿನಿ - Login Page", font=("Arial", 14, "bold"), anchor="center", text_color="black").pack(padx=10)

# Enable window dragging
def start_move(event): root.x, root.y = event.x, event.y
def stop_move(event): root.x, root.y = None, None
def do_move(event): root.geometry(f"+{event.x_root - root.x}+{event.y_root - root.y}")
titlebar.bind("<ButtonPress-1>", start_move)
titlebar.bind("<ButtonRelease-1>", stop_move)
titlebar.bind("<B1-Motion>", do_move)

# ------------------ Background ------------------ #
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()

try:
    # Use the absolute path for testing purposes
    bg_image_raw = Image.open("nandini1.jpeg").resize((screen_width, screen_height))
    bg_image = CTkImage(light_image=bg_image_raw, size=(screen_width, screen_height))
    CTkLabel(root, image=bg_image, text="").place(x=0, y=40)
except FileNotFoundError:
    messagebox.showerror("Error", "Background image file not found. Please check the image path.")
    root.quit()


# ------------------ Login Form ------------------ #
CTkLabel(root, text="ನಂದಿನಿ", font=("Goudy Old Style", 30, "bold"), fg_color="#b2f7ef", text_color="black").pack(pady=(30, 20))

usernameEntry = CTkEntry(root, placeholder_text="Enter your username", height=40, width=300,
                         font=("Arial", 14), fg_color="#b2f7ef", text_color="black")
usernameEntry.pack(pady=(10, 30))

passwordEntry = CTkEntry(root, placeholder_text="Enter your password", height=40, width=300,
                         font=("Arial", 14), fg_color="#b2f7ef", text_color="black", show="*")
passwordEntry.pack(pady=10)

CTkButton(root, text="Login", font=("Arial", 14), height=40, width=300,
          fg_color="#b2f7ef", hover_color="#047857", text_color="black", command=login).pack(pady=(20, 10))

CTkButton(root, text="New Register", font=("Arial", 14), height=40, width=300,
          fg_color="#b2f7ef", text_color="black", hover_color="#cccccc", command=open_register_window).pack(pady=(20, 10))

CTkButton(root, text="Forgot password", font=("Arial", 14), height=40, width=300,
          fg_color="#b2f7ef", text_color="black", hover_color="#cccccc", command=forgot).pack(pady=(20, 10))

CTkButton(root, text="Back to main login", font=("Arial", 14), height=40, width=300,
          fg_color="#b2f7ef", text_color="black", hover_color="#cccccc", command=back).pack(pady=(20, 10))

# Key bindings
root.bind('<Return>', submit_on_enter)
root.bind('<Escape>', lambda e: close_window())

root.mainloop()
