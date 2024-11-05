import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk

# Default file extensions to look for
file_extensions = ['.py', '.ipynb', '.html', '.css', '.js', '.jsx', '.ts', '.tsx', '.rst', '.md']
# Directories to ignore
ignored_directories = ['node_modules','.next']

def is_ignored(path, ignored_dirs, folder_path):
    rel_path = os.path.relpath(path, folder_path)
    for pattern in ignored_dirs:
        if rel_path.startswith(pattern):
            return True
    return False

def parse_local_folder(folder_path):
    tree_str = ""
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignored_directories, folder_path)]

        indent = root.replace(folder_path, '').count(os.sep)
        sub_indent = '    ' * indent
        tree_str += f"{sub_indent}[{os.path.basename(root)}/]\n"

        # Loop over each file in the directory
        for file in files:
            file_path = os.path.join(root, file)
            if not file.startswith('.') and not is_ignored(file_path, ignored_directories, folder_path):  # Ignore hidden and ignored files
                tree_str += f"{sub_indent}    {file}\n"
                if any(file.endswith(ext) for ext in file_extensions):
                    file_paths.append((indent + 1, file_path))
    return tree_str, file_paths

def get_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def retrieve_local_folder_info(folder_path):
    formatted_string = ""

    # Try to read README if it exists
    readme_path = os.path.join(folder_path, 'README.md')
    if os.path.exists(readme_path):
        formatted_string += "README.md:\n```\n" + get_file_content(readme_path) + "\n```\n\n"
    else:
        formatted_string += "README.md: Not found\n\n"

    # Build directory structure and get file paths
    directory_tree, file_paths = parse_local_folder(folder_path)
    formatted_string += f"Directory Structure:\n{directory_tree}\n"

    # Read content of selected files
    for indent, path in file_paths:
        file_content = get_file_content(path)
        formatted_string += '\n' + '    ' * indent + f"{os.path.relpath(path, folder_path)}:\n" + '    ' * indent + '```\n' + file_content + '\n' + '    ' * indent + '```'

    return formatted_string

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_text.delete("1.0", tk.END)  # Clear previous output
        output = retrieve_local_folder_info(folder_path)
        output_text.insert(tk.END, output)  # Display output

def export_text():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output = retrieve_local_folder_info(folder_path)
        folder_name = os.path.basename(folder_path)
        date_str = datetime.now().strftime("%Y%m%d")
        file_name = f"{folder_name}_{date_str}.txt"
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)
        try:
            with open(downloads_path, 'w', encoding='utf-8') as file:
                file.write(output)
            messagebox.showinfo("Export Successful", f"File exported to {downloads_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error exporting file: {str(e)}")

def add_extension():
    new_extension = extension_entry.get().strip()
    if new_extension and new_extension not in file_extensions:
        file_extensions.append(new_extension)
        extensions_listbox.insert(tk.END, new_extension)
        extension_entry.delete(0, tk.END)

def remove_selected_extension():
    selected_indices = extensions_listbox.curselection()
    for index in reversed(selected_indices):
        file_extensions.pop(index)
        extensions_listbox.delete(index)

def add_ignored_directory():
    new_directory = ignored_entry.get().strip()
    if new_directory and new_directory not in ignored_directories:
        ignored_directories.append(new_directory)
        ignored_listbox.insert(tk.END, new_directory)
        ignored_entry.delete(0, tk.END)

def remove_selected_ignored():
    selected_indices = ignored_listbox.curselection()
    for index in reversed(selected_indices):
        ignored_directories.pop(index)
        ignored_listbox.delete(index)

# Set up GUI
root = tk.Tk()
root.title("Local Folder Parser")
root.geometry("700x700")
root.configure(bg="#f0f0f0")

# Apply a modern theme
style = ttk.Style(root)
style.theme_use('clam')

# Create a frame for the buttons
button_frame = ttk.Frame(root, padding="10")
button_frame.pack(fill=tk.X)

# Create Select Folder Button
select_button = ttk.Button(button_frame, text="Select Folder", command=select_folder)
select_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create Export Text Button
export_button = ttk.Button(button_frame, text="Export Text", command=export_text)
export_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a "Made with Love" Button
love_button = ttk.Button(button_frame, text="Made with ❤ or Msth", command=lambda: messagebox.showinfo("Made with Love", "This application was made with ❤ or Msth!"))
love_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Create a frame for the file extensions
extension_frame = ttk.LabelFrame(root, text="Manage File Extensions", padding="10")
extension_frame.pack(pady=10, padx=10, fill=tk.X)

# Entry for adding new file extensions
extension_entry = ttk.Entry(extension_frame)
extension_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

# Button to add new file extension
add_extension_button = ttk.Button(extension_frame, text="Add Extension", command=add_extension)
add_extension_button.grid(row=0, column=1, padx=5, pady=5)

# Button to remove selected file extensions
remove_extension_button = ttk.Button(extension_frame, text="Remove Selected", command=remove_selected_extension)
remove_extension_button.grid(row=0, column=2, padx=5, pady=5)

# Listbox to display current file extensions
extensions_listbox = tk.Listbox(extension_frame, height=5, selectmode=tk.MULTIPLE)
extensions_listbox.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky='ew')
for ext in file_extensions:
    extensions_listbox.insert(tk.END, ext)

# Create a frame for ignored directories
ignored_frame = ttk.LabelFrame(root, text="Manage Ignored Directories", padding="10")
ignored_frame.pack(pady=10, padx=10, fill=tk.X)

# Entry for adding new ignored directory
ignored_entry = ttk.Entry(ignored_frame)
ignored_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

# Button to add new ignored directory
add_ignored_button = ttk.Button(ignored_frame, text="Add Directory", command=add_ignored_directory)
add_ignored_button.grid(row=0, column=1, padx=5, pady=5)

# Button to remove selected ignored directories
remove_ignored_button = ttk.Button(ignored_frame, text="Remove Selected", command=remove_selected_ignored)
remove_ignored_button.grid(row=0, column=2, padx=5, pady=5)

# Listbox to display current ignored directories
ignored_listbox = tk.Listbox(ignored_frame, height=5, selectmode=tk.MULTIPLE)
ignored_listbox.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky='ew')
for ignored in ignored_directories:
    ignored_listbox.insert(tk.END, ignored)

# Create ScrolledText widget for displaying output
output_frame = ttk.Frame(root, padding="10")
output_frame.pack(fill=tk.BOTH, expand=True)

output_label = ttk.Label(output_frame, text="Output:")
output_label.pack(anchor='w')

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=20)
output_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()
