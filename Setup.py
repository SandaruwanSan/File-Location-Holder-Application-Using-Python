from cx_Freeze import setup, Executable
import sys
import os

# Get the directory where setup.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(current_dir, "icon.ico")

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["tkinter", "tkinterdnd2", "win32clipboard", "win32com.client"],
    "excludes": [],
    "include_files": [],
    # Add any additional DLLs or files needed
    "include_msvcr": True,
}

# Base for GUI applications
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="FileLocationManager",
    version="1.0",
    description="File Location Manager Application",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",  # your main script name
            base=base,
            target_name="FileLocationManager.exe",
            icon=icon_path,  # Using the icon from the build folder
        )
    ],
)
