import customtkinter as ctk
import subprocess
import mysql.connector
from tkinter import messagebox
from PIL import Image

# MySQL connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="madhu@123",  # Update as needed
        database="member_data"  # Update as needed
    )

class MemberLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Frameless window without override-redirect flag
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        self.title("Member Login")

        # Background image
        bg_image = Image.open("background2.jpeg").resize((screen_width, screen_height))
        self.bg_image = ctk.CTkImage(light_image=bg_image, size=(screen_width, screen_height))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Custom Title Bar
        # (You can add your custom title bar code here)

        # Center the widgets manually without using a frame
        self.login_label = ctk.CTkLabel(self, text="Member Login", font=("Arial", 22, "bold"), fg_color="black")
        self.login_label.place(relx=0.5, rely=0.28, anchor="center")  # Center the label

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Name", width=250)
        self.name_entry.place(relx=0.5, rely=0.35, anchor="center")  # Center the name entry below the label

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=250)
        self.email_entry.place(relx=0.5, rely=0.42, anchor="center")  # Center the email entry below the name entry

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.password_entry.place(relx=0.5, rely=0.47, anchor="center")  # Center the password entry below the email entry

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login, width=250)
        self.login_button.place(relx=0.5, rely=0.54, anchor="center")  # Center the login button below the password entry

        self.forgot_button = ctk.CTkButton(self, text="Forgot Password?", fg_color="black", hover_color="gray",
                                           command=self.open_reset_password, width=250)
        self.forgot_button.place(relx=0.5, rely=0.61, anchor="center")  # Center the forgot password button below the login button

    def minimize(self):
        self.iconify()  # Minimize the window

    def toggle_maximize(self):
        # Maximize/Restore window size manually
        if self.winfo_height() != self.winfo_screenheight() or self.winfo_width() != self.winfo_screenwidth():
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
            self.maximize_button.config(text="◻")  # Change button text to indicate restore
        else:
            self.geometry("800x600")  # Set to a specific window size
            self.maximize_button.config(text="□")  # Change button text to indicate maximize

    def close(self):
        self.destroy()  # Close the window

    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def move_window(self, event):
        new_x = self.winfo_x() + event.x - self.x_offset
        new_y = self.winfo_y() + event.y - self.y_offset
        self.geometry(f"+{new_x}+{new_y}")

    def login(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not email or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor(buffered=True)

            cursor.execute("SELECT * FROM login WHERE name=%s AND email=%s AND password=%s", (name, email, password))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Success", "Login successful!")
                self.open_next_page()
            else:
                messagebox.showerror("Error", "Invalid credentials")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("DB Error:", err)
            messagebox.showerror("Error", f"Database error!\n{err}")

    def open_next_page(self):
        subprocess.Popen(["python", "info.py"])
        self.after(100, self.withdraw)

    def open_reset_password(self):
        subprocess.Popen(["python", "forgot1.py"])
        self.after(100, self.withdraw)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = MemberLogin()
    app.mainloop()
