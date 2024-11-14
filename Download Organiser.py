import os
import shutil
import logging
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Set up logging
log_file = "file_organizer.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Define file types
file_types = {
    "Photos": [".jpeg", ".jpg", ".png", ".gif", ".bmp", ".tiff"],
    "PDFs": [".pdf"],
    "Music": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"]
}

moved_files = []  # To keep track of moved files for the undo function

# Function to get the Downloads folder path automatically
def get_download_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

# Function to organize files
def organize_files():
    global moved_files
    moved_files = []  # Reset the list for each run

    download_folder = get_download_folder()
    photos_folder = os.path.join(download_folder, "Photos")
    pdfs_folder = os.path.join(download_folder, "PDFs")
    music_folder = os.path.join(download_folder, "Music")
    videos_folder = os.path.join(download_folder, "Videos")

    # Create folders if needed
    for folder in [photos_folder, pdfs_folder, music_folder, videos_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Move files
    for filename in os.listdir(download_folder):
        file_path = os.path.join(download_folder, filename)

        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()

            if file_ext in file_types["Photos"]:
                destination = os.path.join(photos_folder, filename)
                shutil.move(file_path, destination)
                moved_files.append((destination, file_path))
                logging.info(f"Moved {filename} to {photos_folder}")

            elif file_ext in file_types["PDFs"]:
                destination = os.path.join(pdfs_folder, filename)
                shutil.move(file_path, destination)
                moved_files.append((destination, file_path))
                logging.info(f"Moved {filename} to {pdfs_folder}")

            elif file_ext in file_types["Music"]:
                destination = os.path.join(music_folder, filename)
                shutil.move(file_path, destination)
                moved_files.append((destination, file_path))
                logging.info(f"Moved {filename} to {music_folder}")

            elif file_ext in file_types["Videos"]:
                destination = os.path.join(videos_folder, filename)
                shutil.move(file_path, destination)
                moved_files.append((destination, file_path))
                logging.info(f"Moved {filename} to {videos_folder}")

    messagebox.showinfo("Success", "Files have been organized!")
    return moved_files

# Function to undo the last organization
def undo_last_action():
    global moved_files
    if not moved_files:
        messagebox.showinfo("Undo", "No files to undo.")
        return
    
    for destination, original in reversed(moved_files):
        if os.path.exists(destination):
            shutil.move(destination, original)
            logging.info(f"Moved {os.path.basename(destination)} back to {original}")
        else:
            messagebox.showerror("Error", f"File {os.path.basename(destination)} not found for undo.")
    
    moved_files = []  # Clear the list after undo
    messagebox.showinfo("Undo", "Undo complete. Files have been moved back.")

# GUI window to take input
def create_gui():
    root = tk.Tk()
    root.title("File Organizer")

    # Button to organize files
    organize_button = tk.Button(root, text="Organize Files", command=organize_files)
    organize_button.grid(row=0, column=0, padx=10, pady=10)

    # Button to undo last action
    undo_button = tk.Button(root, text="Undo Last Action", command=undo_last_action)
    undo_button.grid(row=1, column=0, padx=10, pady=10)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
