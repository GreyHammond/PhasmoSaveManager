import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time
import zipfile

# Colors based on the palette you provided
DARK_BG = "#000000"  # Background color
LABEL_COLOR = "#D32F2F"  # Red color for text (appropriate for a dark theme)
LABEL_BG_COLOR = "#1A1A1A"  # Slightly offset from black, dark gray
BUTTON_COLOR = "#A2A593"  # Button color (lightest)
BUTTON_TEXT = "#0E0E0B"  # Text on buttons (darkest)

# Paths
save_directory = os.path.join(os.environ['LOCALAPPDATA'], r'..\LocalLow\Kinetic Games\Phasmophobia')
backup_directory = r"C:\Phasmophobia_Backups"

# Create the backup directory if it doesn't exist
os.makedirs(backup_directory, exist_ok=True)

class BackupRestoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phasmophobia Save Manager")
        
        # Get the correct path for the icon
        icon_path = self.resource_path("logo.ico")  

        # Check if the icon file exists
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)  # Set the window icon to logo.ico
        else:
            print(f"Icon file not found at: {icon_path}")  # Print error if not found

        self.root.configure(bg=DARK_BG)  # Set the background color
        self.root.geometry("250x500")  # Adjusted height to fit the image

        # Logo
        self.logo = Image.open(self.resource_path("logo.png")).resize((256, 256))  # Ensure image is resized to 256x256
        self.logo = ImageTk.PhotoImage(self.logo)
        logo_label = tk.Label(root, image=self.logo, bg=DARK_BG)
        logo_label.pack(pady=10)

        # Select Save Folder for Backup
        save_folder_button = tk.Button(root, text="Select Save Folder for Backup", command=self.select_save_folder, bg=BUTTON_COLOR, fg=BUTTON_TEXT)
        save_folder_button.pack(pady=10)

        # Default save folder label (showing last two folders)
        self.save_folder = save_directory  # Set default save folder
        self.save_folder_label = tk.Label(root, text=self.truncate_save_folder(self.save_folder), fg=LABEL_COLOR, bg=LABEL_BG_COLOR, pady=5, padx=5)
        self.save_folder_label.pack(pady=5, padx=5)  # Adjusted padx to match button padding

        # Select Backup Folder Location
        location_button = tk.Button(root, text="Select Backup Folder Location", command=self.select_backup_location, bg=BUTTON_COLOR, fg=BUTTON_TEXT)
        location_button.pack(pady=10)

        # Show only the last folder in the path
        self.backup_location_label = tk.Label(root, text=f"{os.path.basename(backup_directory)}", fg=LABEL_COLOR, bg=LABEL_BG_COLOR, pady=5, padx=5)
        self.backup_location_label.pack(pady=5, padx=5)  # Adjusted padx to match button padding

        # Backup and Restore Buttons
        button_frame = tk.Frame(root, bg=DARK_BG)  # Create a frame for the buttons
        button_frame.pack(pady=10)

        backup_button = tk.Button(button_frame, text="Backup", command=self.backup, bg=BUTTON_COLOR, fg=BUTTON_TEXT)
        backup_button.pack(side='left', expand=True, fill='both', padx=5)

        restore_button = tk.Button(button_frame, text="Restore", command=self.restore, bg=BUTTON_COLOR, fg=BUTTON_TEXT)
        restore_button.pack(side='left', expand=True, fill='both', padx=5)

        # Initialize selected folders
        self.backup_location = ""

    def resource_path(self, relative_path):
        """ Get the absolute path to the resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temporary folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

    def truncate_save_folder(self, full_path):
        """ Truncate the save folder path to show only the last two directories """
        path_parts = full_path.split(os.sep)
        return os.sep.join(path_parts[-2:])  # Get last two parts of the path

    def select_save_folder(self):
        selected_folder = filedialog.askdirectory(title="Select Save Folder", initialdir=self.save_folder)  # Use the current save folder as initial directory
        if selected_folder:
            self.save_folder = selected_folder
            self.save_folder_label.config(text=self.truncate_save_folder(self.save_folder))

    def select_backup_location(self):
        selected_location = filedialog.askdirectory(title="Select Backup Location", initialdir=backup_directory)  # Use the current backup directory as initial directory
        if selected_location:
            self.backup_location = selected_location
            self.backup_location_label.config(text=f"Backup Location: {os.path.basename(self.backup_location)}")  # Show only the folder name

    def backup(self):
        if not self.save_folder:
            messagebox.showwarning("Backup", "Please select a save folder first.")
            return

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_zip_path = os.path.join(self.backup_location or backup_directory, f"backup_{timestamp}.zip")

        # Create a zip file
        with zipfile.ZipFile(backup_zip_path, 'w') as backup_zip:
            for item in os.listdir(self.save_folder):
                if item in ["SaveFile.txt", "saveData.txt"]:  # Backup only these two files
                    file_path = os.path.join(self.save_folder, item)
                    backup_zip.write(file_path, item)

        messagebox.showinfo("Backup", f"Backup completed at: {backup_zip_path}")

    def restore(self):
        if not self.backup_location:
            messagebox.showwarning("Restore", "Please select a backup folder first.")
            return

        # Restore the contents of the zip file back to the save directory
        with zipfile.ZipFile(self.backup_location, 'r') as backup_zip:
            backup_zip.extractall(save_directory)

        messagebox.showinfo("Restore", f"Restore completed from: {self.backup_location}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupRestoreApp(root)
    root.mainloop()
