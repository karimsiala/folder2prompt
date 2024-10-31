import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk

def parse_local_folder(folder_path):
    """
    Parses the local folder and builds a directory tree structure.
    """
    tree_str = ""
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        indent = root.replace(folder_path, '').count(os.sep)
        sub_indent = '    ' * indent
        tree_str += f"{sub_indent}[{os.path.basename(root)}/]\n"

        # Loop over each file in the directory
        for file in files:
            if not file.startswith('.'):  # Ignore hidden files
                file_path = os.path.join(root, file)
                tree_str += f"{sub_indent}    {file}\n"
                if file.endswith(('.py', '.ipynb', '.html', '.css', '.js', '.jsx', '.rst', '.md')):
                    file_paths.append((indent + 1, file_path))
    return tree_str, file_paths

def get_file_content(file_path):
    """
    Reads and returns the content of a file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def retrieve_local_folder_info(folder_path):
    """
    Retrieves information from a local folder, including the directory structure
    and contents of specific files.
    """
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
        formatted_string += '\n' + '    ' * indent + f"{os.path.relpath(path, folder_path)}:\n" + '    ' * indent + '```\n' + file_content + '\n' + '    ' * indent + '```\n'

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

# Set up GUI
root = tk.Tk()
root.title("Local Folder Parser")
root.geometry("800x600")

# Apply a modern theme
style = ttk.Style(root)
style.theme_use('clam')

# Create a frame for the buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Create Select Folder Button
select_button = ttk.Button(button_frame, text="Select Folder", command=select_folder)
select_button.pack(side=tk.LEFT, padx=5)

# Create Export Text Button
export_button = ttk.Button(button_frame, text="Export Text", command=export_text)
export_button.pack(side=tk.LEFT, padx=5)

# Create ScrolledText widget for displaying output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
