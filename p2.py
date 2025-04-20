import customtkinter as ctk
import subprocess
from PIL import Image
import os
import sys

# Helper function to access resources in the packaged app
def resource_path(relative_path):
    # If running as a packaged app
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    else:
        base_path = os.path.dirname(__file__)  # Normal path if running as script
    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MainLoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Frameless full screen
        self.overrideredirect(False)
        self.title('')
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.configure(fg_color="#f1f1f1")

        self.update()  # Ensure screen size is correctly fetched
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Load background image
        bg_image_path = resource_path("background.jpeg")
        bg_image = Image.open(bg_image_path)
        self.bg_image = ctk.CTkImage(light_image=bg_image, size=(screen_width, screen_height))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Custom title bar
        self.title_bar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color="#2c3e50")
        self.title_bar.pack(fill="x", side="top")

        self.title_label = ctk.CTkLabel(self.title_bar, text="ನಂದಿನಿ ಡೈರಿ", text_color="white", font=("Helvetica", 18, "bold"))
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")

        # Center card
        self.label = ctk.CTkLabel(self, text="ನಂದಿನಿ ಡೈರಿ", width=200, height=100, fg_color="#2980b9", font=("Helvetica", 24, "bold"), text_color="black")
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.admin_btn = ctk.CTkButton(self, text="Admin Login", font=("Arial", 16), fg_color="blue", height=45, hover_color="#2980b9", command=self.open_admin_login)
        self.admin_btn.place(relx=0.5, rely=0.6, anchor="center")

        self.member_btn = ctk.CTkButton(self, text="Member Login", font=("Helvetica", 16), fg_color="red", height=45, corner_radius=12, hover_color="#27ae60", command=self.open_member_login)
        self.member_btn.place(relx=0.5, rely=0.7, anchor="center")

    def open_admin_login(self):
        # Using resource_path for login.py (same for member.py)
        login_path = resource_path("login.py")
        subprocess.Popen([sys.executable, login_path])  # Run login.py with the current python interpreter
        self.withdraw()

    def open_member_login(self):
        member_path = resource_path("member.py")
        subprocess.Popen([sys.executable, member_path])  # Run member.py with the current python interpreter
        self.withdraw()

if __name__ == "__main__":
    app = MainLoginApp()
    app.mainloop()
