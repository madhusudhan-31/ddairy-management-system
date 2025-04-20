import mysql.connector
from customtkinter import *
from tkinter import messagebox,Canvas
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess

# ---------------- DATABASE FUNCTION ----------------
import re

def register():
    new_username = usernameEntry.get()
    new_password = passwordEntry.get()
    user_email = emailEntry.get()

    if new_username == "" or new_password == "" or user_email == "":
        messagebox.showerror("Error", "Username, password, and email cannot be empty")
        return

    # ✅ Step 1: Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, user_email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address")
        return

    # ✅ Step 2: Try to send email before registering
    if  send_confirmation_email(user_email):
        messagebox.showerror("succes", "mail sended.")
        return

    # ✅ Step 3: Register user after email success
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="madhu@123",
            database="member_data"
        )
        cursor = conn.cursor()

        # Check for duplicate username
        cursor.execute("SELECT * FROM login WHERE name=%s", (new_username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists!")
        else:
            cursor.execute("INSERT INTO login (name, password, email) VALUES (%s, %s, %s)",
                           (new_username, new_password, user_email))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")

            registerWindow.destroy()
            subprocess.Popen(["python", "login.py"])
            registerWindow.withdraw()

        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")



# ---------------- EMAIL SENDING FUNCTION ----------------
def send_confirmation_email(user_email):
    try:
        sender_email = "madhusudhangowdahg31@gmail.com"  # Replace with your email
        sender_password = "fejs sppy xdew vizh"  # Replace with your email password or app-specific password

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = user_email
        message['Subject'] = 'Registration Successful'

        body = f'''Hello,\n\nYour account has been successfully created in Nandini dairy with the
        username:{usernameEntry.get()}
        password:{passwordEntry.get()}
        mail:{emailEntry.get()}
        Welcome to Nandini Dairy!\n\nBest regards,\nDairy Management Team'''
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, message.as_string())
            print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {e}")

# ---------------- UI STARTS ----------------
registerWindow = CTk()
registerWindow.geometry("900x600")
registerWindow.title("Register")
registerWindow.resizable(False, False)
set_appearance_mode("dark")  # or 'light' or 'system'
set_default_color_theme("green")

# Background gradient effect using Canvas
bg_canvas = Canvas(registerWindow, highlightthickness=0)
bg_canvas.pack(fill="both", expand=True)

def draw_gradient(canvas, width, height, color1, color2):
    canvas.delete("all")
    r1, g1, b1 = registerWindow.winfo_rgb(color1)
    r2, g2, b2 = registerWindow.winfo_rgb(color2)
    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
        canvas.create_line(0, i, width, i, fill=color)

def resize_bg(event=None):
    draw_gradient(bg_canvas, registerWindow.winfo_width(), registerWindow.winfo_height(), "#00c6ff", "#0072ff")

registerWindow.bind("<Configure>", resize_bg)

# ---------------- FORM FRAME ----------------
formFrame = CTkFrame(
    master=registerWindow,
    fg_color="#1e1e2f",  # dark bluish glass color
    corner_radius=20,
    width=400,
    height=450  # Adjusted height to accommodate the email entry
)
formFrame.place(relx=0.5, rely=0.5, anchor="center")

# ---------------- FORM CONTENT ----------------
CTkLabel(formFrame, text="✨ Create Account", font=("Arial", 24, "bold")).pack(pady=(30, 20))

usernameEntry = CTkEntry(formFrame, placeholder_text="Username", font=("Arial", 14),fg_color="white",text_color="black", width=280)
usernameEntry.pack(pady=10)

passwordEntry = CTkEntry(formFrame, placeholder_text="Password", show="*", font=("Arial", 14),fg_color="white", text_color="black",width=280)
passwordEntry.pack(pady=10)

emailEntry = CTkEntry(formFrame, placeholder_text="Email", font=("Arial", 14), fg_color="white", text_color="black",width=280)
emailEntry.pack(pady=10)

registerButton = CTkButton(formFrame, text="Register", command=register, width=200, height=40, corner_radius=10)
registerButton.pack(pady=(30, 10))

CTkLabel(formFrame, text="Already have an account?", font=("Arial", 12), text_color="gray").pack(pady=(10, 0))

registerWindow.mainloop()
