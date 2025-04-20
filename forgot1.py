import customtkinter as ctk
import smtplib
import random
import mysql.connector
from tkinter import messagebox
from PIL import Image
import subprocess

# Email credentials
SENDER_EMAIL = "madhusudhangowdahg31@gmail.com"
SENDER_PASSWORD = "fejs sppy xdew vizh"

# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="madhu@123",
        database="member_data"
    )

class ResetPassword(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Reset Password")
        self.geometry("900x600")
        self.resizable(False, False)
        self.otp = None

        # Load background image
        bg_image = Image.open("background2.jpeg").resize((900, 600))
        self.bg_image = ctk.CTkImage(light_image=bg_image, size=(900, 600))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Heading
        self.heading = ctk.CTkLabel(self, text="Reset Password via Email", font=("Arial", 24, "bold"))
        self.heading.place(relx=0.5, rely=0.15, anchor="center")

        # Email entry
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Enter your email", width=300)
        self.email_entry.place(relx=0.5, rely=0.3, anchor="center")

        # OTP entry
        self.otp_entry = ctk.CTkEntry(self, placeholder_text="Enter OTP", width=300)
        self.otp_entry.place(relx=0.5, rely=0.4, anchor="center")

        # New password entry
        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="New Password", show="*", width=300)
        self.new_password_entry.place(relx=0.5, rely=0.5, anchor="center")

        # Send OTP button
        self.send_otp_btn = ctk.CTkButton(self, text="Send OTP", command=self.send_otp, width=300)
        self.send_otp_btn.place(relx=0.5, rely=0.6, anchor="center")

        # Reset button
        self.reset_btn = ctk.CTkButton(self, text="Reset Password", command=self.reset_password, width=300)
        self.reset_btn.place(relx=0.5, rely=0.7, anchor="center")

        # Status label
        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.place(relx=0.5, rely=0.8, anchor="center")

    def send_otp(self):
        email = self.email_entry.get().strip()
        if not email:
            self.status_label.configure(text="Please enter your email", text_color="red")
            return

        self.otp = str(random.randint(100000, 999999))
        print(f"[DEBUG] OTP sent to {email}: {self.otp}")

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            message = f"Subject: OTP for Password Reset\n\nYour OTP is: {self.otp}"
            server.sendmail(SENDER_EMAIL, email, message)
            server.quit()
            self.status_label.configure(text="OTP sent!", text_color="green")
        except Exception as e:
            print("Email error:", e)
            self.status_label.configure(text="Failed to send OTP", text_color="red")

    def reset_password(self):
        entered_otp = self.otp_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        email = self.email_entry.get().strip()

        if not self.otp or entered_otp != self.otp:
            self.status_label.configure(text="Invalid OTP!", text_color="red")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("UPDATE login SET Password = %s WHERE Email = %s", (new_password, email))
            conn.commit()

            if cursor.rowcount == 0:
                self.status_label.configure(text="Email not found in database", text_color="red")
            else:
                self.status_label.configure(text="Password reset successful!", text_color="green")
                self.clear_fields()
                subprocess.Popen(["python", "main.py"])
                self.withdraw()

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Database Error:", err)
            self.status_label.configure(text="Database error", text_color="red")

    def clear_fields(self):
        self.email_entry.delete(0, 'end')
        self.otp_entry.delete(0, 'end')
        self.new_password_entry.delete(0, 'end')

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ResetPassword()
    app.mainloop()
