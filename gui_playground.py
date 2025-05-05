import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

root = tk.Tk()
root.minsize(800,400) # Not strictly enforced in Linux.

frame_loading = ttk.Frame(root)
frame_error = ttk.Frame(root)
frame_results = ttk.Frame(root)

# Header in root to avoid replication.
label_header = ttk.Label(root, 
                         text="Codetown Vote Display",
                         anchor='center',
                         font='bold')
label_instructions = ttk.Label(frame_loading, 
                               text="Please select a file to load.\n\n"
                                    "Either choose a text file from the drop-down menu "
                                    "or click the 'Find my file' button to navigate to your file "
                                    "in its directory.\n\n"
                                    "Once you're satisfied with your file chosen, "
                                    "press the 'Load file' button.")
button_file_finder = ttk.Button(frame_loading, 
                                text="Find my file")
combobox_files_in_current_dir = ttk.Combobox(frame_loading)
button_file_load = ttk.Button(frame_loading, 
                              text="Load file")
label_file_selected = ttk.Label(frame_loading, 
                                text="File selected:")

frame_loading.configure(padding=5, borderwidth=2)



# Grid behaviour for widgets.
# Root widgets
label_header.grid(column=0, row=0, columnspan=1, rowspan=1, pady=(0, 30), sticky='nsew')
frame_loading.grid(column=0, row=1, sticky='nsew')

# frame_loading widgets.
label_instructions.grid(column=0, row=0, columnspan=5, rowspan=1, pady=(0,30), sticky='nsew')
combobox_files_in_current_dir.grid(column=2, row=1, columnspan=3, rowspan=1, sticky='nsew')
button_file_finder.grid(column=0, row=1, columnspan=1, rowspan=1, sticky='nsew')
label_file_selected.grid(column=0, row=2, columnspan=5, pady=(10,10), sticky='nsew')
button_file_load.grid(column=0, row=3, columnspan=1, rowspan=1, sticky='nsew')

# Frame resizing code.
# Resize properties for <Root> widgets
root.columnconfigure(0, weight=1)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=3) # Main body row grows at twice the rate of the header row.

# Resize properties for <frame_loading> widgets
# Must call before using grid_size() value-check.
frame_loading.update_idletasks()
# Iterate through frame columns and rows to set weight=1, allowing for scaling with resize.
for i in range(frame_loading.grid_size()[0]):
    frame_loading.columnconfigure(i, weight=1)
for i in range(frame_loading.grid_size()[1]):
    frame_loading.rowconfigure(i, weight=1)



# Call file dialog window with appropriate title and file-type restrictions.
# Set the text of label_file_selected based on the path of the file selected.
# TODO: OVERRIDE depending on last chosen file- this or combobox; boolean flag?
def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a File", 
                                           filetypes=[("Text files", "*.txt"), 
                                                      ("All files", "*.*")])
    if file_path:
        label_file_selected.config(text=f"File selected: {file_path}")

# Widget bindings
# Bindings for <frame_loading> widgets
button_file_finder.config(command=open_file_dialog)

root.mainloop()