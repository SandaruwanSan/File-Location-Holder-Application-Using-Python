import tkinter as tk
from tkinter import ttk, messagebox
import tkinterdnd2
from tkinter import filedialog
import shutil
import os
import win32clipboard
import sys

#This Programme Was Created using AI and Made By K.P.M.S.B. Karunarathna.
#Faculty of Computing and Technology
#University of Kelaniya
#Copyright © 2025 All Rights Reserved.
class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SR Cafe Copy-Past Manager by SR Corp")
        self.root.geometry("600x400")

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Store file paths
        self.file_paths = []

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create and configure the listbox for file paths
        self.listbox_frame = ttk.LabelFrame(self.main_frame, text="File Locations", padding="5")
        self.listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.listbox_frame, selectmode=tk.EXTENDED)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.configure(yscrollcommand=scrollbar.set)

        # Make listbox a drop target
        self.listbox.drop_target_register(tkinterdnd2.DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.drop_files)

        # Buttons frame
        self.button_frame = ttk.Frame(self.main_frame, padding="5")
        self.button_frame.pack(fill=tk.X, pady=5)

        # Add buttons
        ttk.Button(self.button_frame, text="Add Files", command=self.browse_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Remove Selected", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Copy Files", command=self.copy_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Copy to Clipboard", command=self.copy_files_to_clipboard).pack(side=tk.LEFT,
                                                                                                           padx=5)
        ttk.Button(self.button_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)

    def on_closing(self):
        """Handle window closing event"""
        self.root.quit()
        self.root.destroy()

    def drop_files(self, event):
        """Handle dropped files"""
        files = self.listbox.tk.splitlist(event.data)
        for file in files:
            if file not in self.file_paths:
                self.file_paths.append(file)
                self.listbox.insert(tk.END, file)

    def browse_files(self):
        """Open file browser to select files"""
        files = filedialog.askopenfilenames(title="Select Files")
        for file in files:
            if file not in self.file_paths:
                self.file_paths.append(file)
                self.listbox.insert(tk.END, file)

    def remove_selected(self):
        """Remove selected items from listbox"""
        selected = self.listbox.curselection()
        for index in reversed(selected):
            self.file_paths.pop(index)
            self.listbox.delete(index)

    def clear_all(self):
        """Clear all items from listbox"""
        self.listbox.delete(0, tk.END)
        self.file_paths.clear()

    def copy_files(self):
        """Copy selected files to a new location"""
        if not self.file_paths:
            messagebox.showwarning("Warning", "No files selected to copy!")
            return

        # Ask for destination directory
        dest_dir = filedialog.askdirectory(title="Select Destination Directory")
        if not dest_dir:
            return

        try:
            # Copy each file
            for file_path in self.file_paths:
                if os.path.exists(file_path):
                    shutil.copy2(file_path, dest_dir)
            messagebox.showinfo("Success", "Files copied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error copying files: {str(e)}")

    def copy_files_to_clipboard(self):
        """Copy selected files to Windows clipboard for pasting in Explorer"""
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No items selected!")
            return

        try:
            # Get selected paths
            selected_paths = [self.file_paths[index] for index in selected]

            # Convert paths to the format required by Windows
            offset = len(''.join(selected_paths)) + 1

            # Format the string for CF_HDROP
            dropfiles = (
                b'\x14\x00\x00\x00'  # DROPFILES.pFiles
                b'\x00\x00\x00\x00'  # DROPFILES.pt.x
                b'\x00\x00\x00\x00'  # DROPFILES.pt.y
                b'\x00\x00\x00\x00'  # DROPFILES.fNC
                b'\x01\x00\x00\x00'  # DROPFILES.fWide (1 for Unicode)
            )

            # Add file paths in Unicode format
            data = dropfiles + ''.join(path + '\0' for path in selected_paths).encode('utf-16le') + b'\0\0'

            # Open and set clipboard data
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, data)
            win32clipboard.CloseClipboard()

            messagebox.showinfo("Success", "Files copied to clipboard! You can now paste them in Windows Explorer.")

        except Exception as e:
            messagebox.showerror("Error", f"Error copying files to clipboard: {str(e)}")
        finally:
            try:
                win32clipboard.CloseClipboard()
            except:
                pass


def main():
    if len(sys.argv) > 1:
        print("This application doesn't accept command line arguments.")
        sys.exit(1)

    root = tkinterdnd2.Tk()

    app = FileManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


