from cx_Freeze import setup, Executable
import sys

# Dependencies and files to include
build_exe_options = {
    "packages": ["os", "subprocess", "tkinter", "customtkinter", "PIL", "mysql", "mysql.connector"],
    "include_files": [
        "background.jpeg",
        "login.py",
        "member.py",
        "database.py",
        "database1.py",
        "dairy.jpeg",
        "main.py",
        "milk.py",
        "mem.py",
        # add other images and Python files as needed
    ],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="NandiniDairy",
    version="1.0",
    description="Nandini Dairy Management System",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="NandiniDairy.exe")]
)
