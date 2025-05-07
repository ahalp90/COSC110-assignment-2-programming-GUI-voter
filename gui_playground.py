# def get_txt_files_in_cwd():
#     txt_files_cwd = []
#     try:
#         cwd = os.getcwd()
#         for item_name in os.listdir(cwd):
#             if item_name.endswith(".txt"):
#                 full_path = os.path.join(cwd, item_name)
#                 if os.path.isfile(full_path):
#                     txt_files_cwd.append(item_name)
#     except FileNotFoundError:
#         print(f"The file {item_name} could not be found.\n"
#                 f"Please try again.")
#     except PermissionError:
#         print(f"Error: You don't have permission to access the file {item_name}.\n"
#                 f"Please try again.")
#     except Exception as e: # General error catcher
#         print(f" An unexpected error occured. Please try again.\n"
#                 f"Error: {type(e).__name__}. Error details: {e}.")
    
#     return txt_files_cwd

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

root = tk.Tk()
root.title("Codetown Vote Counter")
root.minsize(800,400) # Not strictly enforced in Linux.

selected_file_path = tk.StringVar()

frame_loading = ttk.Frame(root)
frame_load_output = ttk.Frame(root)

# Header in root to avoid replication if additional frames are added down the track.
label_header = ttk.Label(root, 
                         text="Codetown Vote Display",
                         anchor='center',
                         font='bold')

# Loading frame widgets.
label_instructions = ttk.Label(frame_loading, 
                               text="Please select a file to load.\n\n"
                                    "Either choose a text file from the drop-down menu "
                                    "or click the 'Find my file' button to navigate to your file "
                                    "in its directory.\n\n"
                                    "Once you're satisfied with your file chosen, "
                                    "press the 'Load file' button.",
                                    wraplength=700, # Wrap to frame minwidth minus a bit of buffer.
                                    justify=tk.LEFT)
button_file_finder = ttk.Button(frame_loading, 
                                text="Find my file")
button_file_load = ttk.Button(frame_loading, 
                              text="Load file")
label_file_selected = ttk.Label(frame_loading, 
                                text="No file currently selected", 
                                wraplength=700, # Wrap to frame minwidth minus a bit of buffer.
                                anchor='w')

# Text output widget for display vote count/error messages, and x/y scrollbars for it.
text_loaded_output = tk.Text(frame_load_output, 
                              height=10, 
                              borderwidth=1, 
                              relief=tk.FLAT, 
                              bg='white', 
                              state=tk.DISABLED,
                              wrap=tk.NONE)

scrollbar_x = ttk.Scrollbar(frame_load_output, orient=tk.HORIZONTAL, command=text_loaded_output.xview)
scrollbar_y = ttk.Scrollbar(frame_load_output, orient=tk.VERTICAL, command=text_loaded_output.yview)

text_loaded_output.config(xscrollcommand=scrollbar_x.set,
                           yscrollcommand=scrollbar_y.set)

# Configure frame borders for frame_loading and frame_load_output.
frame_loading.configure(padding=5, borderwidth=2)
frame_load_output.configure(padding=5)



# Grid behaviour for widgets.
# Root widgets
# <label_header> is in a separate grid in case of refactoring for additional frames.
label_header.grid(column=0, row=0, pady=(10, 10), sticky='ew')
frame_loading.grid(column=0, row=1, sticky='nsew')
frame_load_output.grid(column=0, row=2, columnspan=5, sticky='nsew')

# frame_loading widgets.
label_instructions.grid(column=0, row=0, columnspan=5, rowspan=1, pady=(0,30), sticky='nsew')
label_file_selected.grid(column=0, row=2, columnspan=4, rowspan=1, pady=(10,10), sticky='nsew')
button_file_finder.grid(column=4, row=1, columnspan=1, rowspan=1, pady=(5,5), sticky='nsew')
button_file_load.grid(column=4, row=2, columnspan=1, rowspan=1, pady=(5,5), sticky='nsew')

# frame_load_output widgets (Text and Scrollbars).
text_loaded_output.grid(column=0, row=0, sticky='nsew')
scrollbar_y.grid(column=1, row=0, columnspan=1, rowspan=3, sticky='ns')
scrollbar_x.grid(column=0, row=1, columnspan=5, rowspan=1, sticky='ew')


# Frame resizing code.
# Resize properties for <Root> widgets
root.columnconfigure(0, weight=1) # Root needs to expand as the container for all frames.
root.rowconfigure(0, weight=0) # Header doesn't epand.
root.rowconfigure(1, weight=1) # Main body frame expands.
root.rowconfigure(2, weight=1) # Output text frame expands.


# Resize properties for <frame_loading> widgets
# Must call before using grid_size() value-check.
frame_loading.update_idletasks()
# Iterate through frame columns and rows to set weight=1, 
# avoiding hardcoding here to account for ongoing changes in grid code.
for i in range(frame_loading.grid_size()[0]):
    frame_loading.columnconfigure(i, weight=1)
for i in range(frame_loading.grid_size()[1]):
    frame_loading.rowconfigure(i, weight=1)

# Resize properties for output text frame.
frame_load_output.columnconfigure(0, weight=1)
frame_load_output.rowconfigure(0, weight=1)

# Call file dialog window with appropriate title and file-type restrictions.
# Set the text of label_file_selected based on the file selected;
# strip the path on the text for non-technical users.
# Return file_path
def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a File", 
                                           filetypes=[("Text files", "*.txt"), 
                                                      ("All files", "*.*")])
    if file_path:
        selected_file_path.set(file_path)
        label_file_selected.config(text=f"File selected: {os.path.basename(file_path)}")
        return file_path






# Widget bindings
# Bindings for <frame_loading> widgets
button_file_finder.config(command=open_file_dialog)

# button_file_load.config(command=load_file(filename))


root.mainloop()




# https://tkdocs.com/tutorial/widgets.html