import tkinter as tk
from tkinter import filedialog

import waitparse  # Import your waitparse module

def select_input_folder():
    folder = filedialog.askdirectory()
    waitparse.process_input_folder(folder)  # Call the function from waitparse.py
    input_folder_label_text.set(f'Input Folder: {folder}')

def select_backup_folder():
    folder = filedialog.askdirectory()
    waitparse.process_backup_folder(folder)  # Call the function from waitparse.py
    backup_folder_label_text.set(f'Backup Folder: {folder}')

def select_output_folder():
    folder = filedialog.askdirectory()
    waitparse.process_output_folder(folder)  # Call the function from waitparse.py
    output_folder_label_text.set(f'Output Folder: {folder}')

def start_processing():
    waitparse.main()

root = tk.Tk()

# Add buttons for folder selection
input_button = tk.Button(root, text="Select Input Folder", command=select_input_folder)
input_button.pack()

backup_button = tk.Button(root, text="Select Backup Folder", command=select_backup_folder)
backup_button.pack()

output_button = tk.Button(root, text="Select Output Folder", command=select_output_folder)
output_button.pack()

# Add labels to display folder paths
input_folder_label_text = tk.StringVar()
input_folder_label = tk.Label(root, textvariable=input_folder_label_text)
input_folder_label.pack()

backup_folder_label_text = tk.StringVar()
backup_folder_label = tk.Label(root, textvariable=backup_folder_label_text)
backup_folder_label.pack()

output_folder_label_text = tk.StringVar()
output_folder_label = tk.Label(root, textvariable=output_folder_label_text)
output_folder_label.pack()

# Add a button for starting the processing
start_processing_button = tk.Button(root, text="Start Processing", command=start_processing)
start_processing_button.pack()

root.mainloop()