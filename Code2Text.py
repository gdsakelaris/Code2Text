import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk
import subprocess


def read_and_append(file_path, output_file):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
            relative_path = os.path.relpath(file_path, directory_path)
            output_file.write('-' * 9 + '\n' + relative_path + ':\n\n')
            for line in content:
                output_file.write('  ' + line)
            output_file.write('\n')
    except UnicodeDecodeError:
        print(f"Could not read file {file_path} due to a UnicodeDecodeError.")


def traverse_directory(directory_path):
    file_paths = []
    exclude_dirs = {".git", "__pycache__", "venv",
                    "node_modules"}  # add more if needed
    # add more file extensions to exclude
    exclude_extensions = {".png", ".jpg", ".pdf", ".docx"}
    for root, dirs, files in os.walk(directory_path):
        # exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            file_path = os.path.join(root, file)
            _, file_extension = os.path.splitext(file)
            if file_extension.lower() not in exclude_extensions:
                file_paths.append(file_path)
    return file_paths


def remove_selected():
    selected_indices = listbox.curselection()
    # Reverse to avoid index shifting during deletion
    for index in selected_indices[::-1]:
        selected_file = listbox.get(index)
        listbox2.insert('end', selected_file)  # Add to the second listbox
        listbox.delete(index)  # Remove from the first listbox


# Other options: "equilux", "kroc", "radiance", "arc" etc.
root = ThemedTk(theme="clearlooks")
root.title('Code2Text | © 2023 Daniel Sakelaris')

directory_path = filedialog.askdirectory()
if not directory_path:
    print("No directory chosen. Exiting.")
    exit()

# Extract the directory name from the selected path
directory_name = os.path.basename(directory_path)

def move_up():
    selected_indices = listbox2.curselection()
    for index in selected_indices:
        if index != 0:  # Not the first item
            value = listbox2.get(index)
            listbox2.delete(index)
            listbox2.insert(index - 1, value)
            listbox2.selection_set(index - 1)  # Keep the item selected


def move_down():
    selected_indices = listbox2.curselection()
    # Start from the end to avoid index shifting
    for index in selected_indices[::-1]:
        if index != listbox2.size() - 1:  # Not the last item
            value = listbox2.get(index)
            listbox2.delete(index)
            listbox2.insert(index + 1, value)
            listbox2.selection_set(index + 1)  # Keep the item selected


def move_to_top():
    selected_indices = listbox2.curselection()
    for index in selected_indices:
        value = listbox2.get(index)
        listbox2.delete(index)
        listbox2.insert(0, value)
        listbox2.selection_set(0)


def move_to_bottom():
    selected_indices = listbox2.curselection()
    for index in selected_indices[::-1]:
        value = listbox2.get(index)
        listbox2.delete(index)
        listbox2.insert(tk.END, value)
        listbox2.selection_set(listbox2.size() - 1)


##def generate_output_file():
##    output_file_path = filedialog.asksaveasfilename(
##        defaultextension=".txt", initialfile="Code2Text_output_file", filetypes=[("Text files", "*.txt")])
##    if output_file_path:  # If a file path is chosen
##        with open(output_file_path, 'w') as output_file:
##            for file in listbox2.get(0, 'end'):
##                read_and_append(file, output_file)
##        time.sleep(2)  # Delay for 2 seconds
##        subprocess.run(['start', output_file_path], shell=True)
def generate_output_file():
    default_file_name = directory_name + "2.txt"
    output_file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", initialfile=default_file_name, filetypes=[("Text files", "*.txt")])
    if output_file_path:  # If a file path is chosen
        with open(output_file_path, 'w') as output_file:
            for file in listbox2.get(0, 'end'):
                read_and_append(file, output_file)
        time.sleep(1)  # Delay for 1 seconds
        subprocess.run(['start', output_file_path], shell=True)


# Adjust window size
root.geometry('1010x520')

frame1 = ttk.Frame(root)
frame1.pack(fill='x')

lbl1 = ttk.Label(frame1, text='Select Files to Include:',
                 font=('Consolas', 12))
lbl1.pack(side='left')

frame2 = ttk.Frame(root)
frame2.pack(fill='both', expand=True)

listbox_frame = ttk.Frame(frame2)
listbox_frame.pack(side='left', fill='both', expand=True)

scrollbar = ttk.Scrollbar(listbox_frame)
scrollbar.pack(side='right', fill='y')

listbox = tk.Listbox(
    listbox_frame, yscrollcommand=scrollbar.set, selectmode='multiple')
listbox.pack(side='left', fill='both', expand=True)

for file in traverse_directory(directory_path):
    listbox.insert('end', file)

scrollbar.config(command=listbox.yview)

frame3 = ttk.Frame(root)
frame3.pack(fill='both', expand=True)

btn1_frame = ttk.Frame(frame3)
btn1_frame.pack(side='top', pady=10)

btn1 = ttk.Button(btn1_frame, text='Include Selected', command=remove_selected)
btn1.pack(side='left', fill='x')

listbox2_frame = ttk.Frame(frame3)
listbox2_frame.pack(side='left', fill='both', expand=True)

scrollbar2 = ttk.Scrollbar(listbox2_frame)
scrollbar2.pack(side='right', fill='y')

listbox2 = tk.Listbox(listbox2_frame, yscrollcommand=scrollbar2.set)
listbox2.pack(side='left', fill='both', expand=True)

scrollbar2.config(command=listbox2.yview)

frame4 = ttk.Frame(root)
frame4.pack(fill='x')

btn3 = ttk.Button(frame4, text='Move Up', command=move_up)
btn3.pack(side='left')

btn4 = ttk.Button(frame4, text='Move Down', command=move_down)
btn4.pack(side='left')

btn5 = ttk.Button(frame4, text='Move to Top', command=move_to_top)
btn5.pack(side='left')

btn6 = ttk.Button(frame4, text='Move to Bottom', command=move_to_bottom)
btn6.pack(side='left')

btn2 = ttk.Button(frame4, text='Generate Output File',
                  command=generate_output_file)
btn2.pack(side='right')

# Display instructions
# instructions = '''
# The "CTXT" application allows you to select and arrange files from a directory and generate a consolidated output file with the selected files' contents.
##
# 1. Choose Directory:
# - The application will open a file dialog asking you to select a directory.
# - Browse and select the directory that contains the files you want to process.
# - Click "OK" or "Select Folder" to proceed.
# - Note: If you cancel or close the file dialog without selecting a directory, the application will exit.
##
# 2. Select Files:
# - In the application window, you will see a list of files in the selected directory.
# - Use the scrollbar on the right to scroll through the list if necessary.
# - To include files, click on the desired files to select them.
# - You can select multiple files by holding down the Ctrl key (or Command key on macOS) while clicking.
# - Once you have selected the files you want to include, click the "Include Selected" button.
# - The selected files will be moved to the "Included" section on the right.
##
# 3. Rearrange Files (Optional):
# - If you want to rearrange the order of the included files, you can use the following buttons in the "Included" section:
# - "Move Up": Moves the selected file(s) one position up.
# - "Move Down": Moves the selected file(s) one position down.
# - "Move to Top": Moves the selected file(s) to the top of the list.
# - "Move to Bottom": Moves the selected file(s) to the bottom of the list.
##
# 4. Generate Output File:
# - Click the "Generate Output File" button to create a consolidated output file.
# - A file dialog will open, allowing you to choose the location and name for the output file.
# - By default, the file will be saved as a .txt file.
##
# 5. Exit the Application:
# - You can close the application window to exit the program.
# '''
##
# Create a text widget to display the instructions
# text_widget = tk.Text(root, wrap='word', font=('Arial', 12), spacing1=5)
# text_widget.insert('1.0', instructions)
# text_widget.configure(state='disabled')
# text_widget.pack(fill='both', expand=True)

root.mainloop()
