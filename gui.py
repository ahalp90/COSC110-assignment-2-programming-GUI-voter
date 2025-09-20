"""
GUI frontend for Codetown Vote Display.

This module provides a Tkinter-based graphical interface for loading and
displaying election results.
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from vote_processor import BordaVoteProcessor


class VoteCounterGUI:
    """Tkinter GUI for the Codetown Vote Counter application."""
    
    def __init__(self):
        """Initialize the GUI and all its components."""
        self.vote_processor = BordaVoteProcessor()
        
        # Initialise the main Tkinter window.
        self.root = tk.Tk()
        self.root.title("Codetown Vote Counter")
        self.root.minsize(800, 500)  # Minimum window size; not strictly enforced in Linux.
        
        # Tkinter StringVar to hold the path of the selected file.
        self.selected_file_path = tk.StringVar()
        
        # Create all widgets and layout
        self.create_widgets()
        self.configure_layout()
        self.configure_bindings()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Create layout frames.
        self.frame_loading = ttk.Frame(self.root)
        self.frame_load_output = ttk.Frame(self.root)
        
        # WIDGETS.
        # Main header.
        # Header in root to avoid replication if additional frames are added in an update.
        self.label_header = ttk.Label(self.root,
                                      text="Codetown Vote Display",
                                      anchor='center',
                                      font='bold')
        
        # Loading frame widgets.
        self.label_instructions = ttk.Label(
            self.frame_loading,
            text="Please select a file to load.\n\n"
            "Click the 'Find my file' button to navigate to your file "
            "in its directory.\n\n"
            "Once you're satisfied with your file chosen, press the 'Load file' button.",
            wraplength=700,  # Wrap to frame minwidth minus a bit of buffer.
            justify=tk.LEFT)
        
        self.button_file_finder = ttk.Button(self.frame_loading,
                                            text="Find my file")
        
        self.button_file_load = ttk.Button(self.frame_loading,
                                          text="Load file")
        
        self.label_file_selected = ttk.Label(
            self.frame_loading,
            text="No file currently selected",
            wraplength=700,  # Wrap to frame minwidth minus a bit of buffer.
            anchor='w')
        
        # Output display frame widgets (frame_load_output).
        # Text widget displays vote count/error messages, and y scrollbar for it.
        self.text_loaded_output = tk.Text(self.frame_load_output,
                                         height=10,
                                         borderwidth=1,
                                         relief=tk.FLAT,
                                         bg='white',
                                         state=tk.DISABLED,  # Initially read-only.
                                         wrap=tk.WORD)
        
        # Vertical scrollbar for the text_loaded_output widget.
        self.scrollbar_y = ttk.Scrollbar(
            self.frame_load_output, orient=tk.VERTICAL, command=self.text_loaded_output.yview)
        
        # Configure the Text widget to use the scrollbar.
        self.text_loaded_output.config(yscrollcommand=self.scrollbar_y.set)
        
        # Configure frame borders for frame_loading and frame_load_output.
        self.frame_loading.configure(padding=5, borderwidth=2)
        self.frame_load_output.configure(padding=5)
    
    def configure_layout(self):
        """Configure the grid layout for all widgets."""
        # GRID LAYOUT FOR WIDGETS.
        # Root widgets.
        # <label_header> is in a separate grid in case of refactoring for additional frames.
        self.label_header.grid(column=0, row=0, pady=(10, 10), sticky='ew')
        self.frame_loading.grid(column=0, row=1, sticky='nsew')
        self.frame_load_output.grid(column=0, row=2, columnspan=5, sticky='nsew')
        
        # frame_loading widgets.
        self.label_instructions.grid(column=0,
                                    row=0,
                                    columnspan=5,
                                    rowspan=1,
                                    pady=(0, 30),
                                    sticky='nsew')
        self.label_file_selected.grid(column=0,
                                     row=2,
                                     columnspan=4,
                                     rowspan=1,
                                     pady=(10, 10),
                                     sticky='nsew')
        self.button_file_finder.grid(column=4,
                                    row=1,
                                    columnspan=1,
                                    rowspan=1,
                                    pady=(5, 5),
                                    sticky='nsew')
        self.button_file_load.grid(column=4,
                                  row=2,
                                  columnspan=1,
                                  rowspan=1,
                                  pady=(5, 5),
                                  sticky='nsew')
        
        # frame_load_output widgets (Text and Scrollbar).
        self.text_loaded_output.grid(column=0,
                                    row=0,
                                    sticky='nsew')
        self.scrollbar_y.grid(column=1,
                            row=0,
                            columnspan=1,
                            rowspan=3,
                            sticky='ns')
        
        # FRAME RESIZING BEHAVIOUR
        # Resize properties for <Root> widgets
        # Root needs to expand as the container for all frames.
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)  # Header doesn't expand.
        self.root.rowconfigure(1, weight=1)  # Main body frame expands.
        self.root.rowconfigure(2, weight=1)  # Output text frame expands.
        
        # Resize properties for <frame_loading> widgets.
        # Iterative due to facilitate ongoing UI tinkering
        # Must call before using grid_size() value-check.
        self.frame_loading.update_idletasks()
        # Iterate through frame columns and rows to set weight=1,
        # All columns expand equally.
        for i in range(self.frame_loading.grid_size()[0]):
            self.frame_loading.columnconfigure(i, weight=1)
        # All rows expand equally.
        for i in range(self.frame_loading.grid_size()[1]):
            self.frame_loading.rowconfigure(i, weight=1)
        
        # Resize properties for output text frame.
        # Text widget's column and row expand equally.
        self.frame_load_output.columnconfigure(0, weight=1)
        self.frame_load_output.rowconfigure(0, weight=1)
    
    def configure_bindings(self):
        """Configure button bindings to their callback functions."""
        # Connect button clicks to their associated functions.
        self.button_file_finder.config(command=self.open_file_dialog)
        self.button_file_load.config(command=self.handle_load_file_click)
    
    def display_in_output_text(self, message_text):
        """
        Updates the content of the output Text widget.

        Runs through the following sequence when called:
        (1) Momentarily set the output textbox to normal (not read-only) to enable 
            editing.
        (2) Delete all text from the first line to the end.
        (3) Inserts the desired text.
        (4) Renders the widget read-only again.

        Arguments:
            message_text (string): The text to display in the output widget.
        """
        self.text_loaded_output.config(state=tk.NORMAL)
        self.text_loaded_output.delete('1.0', tk.END)
        self.text_loaded_output.insert(tk.END, message_text)
        self.text_loaded_output.config(state=tk.DISABLED)
    
    def open_file_dialog(self):
        """
        Opens a file dialogue for the user to select an input file.

        Updates the 'selected_file_path' StringVar and the 'label_file_selected'
            widget with the chosen file's path.
        Only the basename--filename and filetype stripped of directory--is 
            displayed. This is for brevity and user-friendliness.
        """
        # Open file system dialogue, defaulting to only show <.txt> files.
        filename = filedialog.askopenfilename(title="Select a File",
                                             filetypes=[("Text files", "*.txt"),
                                                       ("All files", "*.*")])
        if filename:  # If a file was selected to open.
            self.selected_file_path.set(filename)
            self.label_file_selected.config(
                text=f"File selected: {os.path.basename(filename)}")
    
    def handle_load_file_click(self):
        """
        Handles the 'Load file' button click event.

        Retrieves the selected file's path, calls load_file(filename) to attempt to 
            load and process the file, and then displays either the Borda-counted 
            and sorted election results or an error message in the output text area.

        Passes filename to load_file(filename). <filename> is derived here from a 
            global variable rather than being received as an argument due to its 
            role in the GUI and maintainability concerns related to the likelihood 
            of ongoing tweaking of the GUI.
        """
        filename = self.selected_file_path.get()
        
        # Handle the case that a file load is attempted before a file is selected.
        # Prints to screen rather than raising an exception as this is normal 
        # program operation behaviour.
        if not filename:
            self.display_in_output_text(
                "You've tried to load a file but haven't yet selected one to load.\n\n"
                "Please select a file using 'Find my file'.")
            return
        
        try:
            # Call load_file(filename) and assign the output to a variable.
            sorted_borda_dict = self.vote_processor.load_file(filename)
            
            # Format the election results dictionary for line-by-line display.
            output_list = []
            
            for candidate, score in sorted_borda_dict.items():
                output_list.append(f"{candidate}: {score}")
            
            output_message = (
                f"Sucessfully loaded and processed: {os.path.basename(filename)}\n\n"
                "Borda Count Results of the Codetown Election\n\n"
                "Candidate: Score\n\n"
                # Print the lists's string values as successive on-screen lines.
                f"{'\n'.join(output_list)}")
            
            self.display_in_output_text(output_message)
        
        # Receive all raised exceptions from child functions, as well as any 
        # unexpected exception originating here.
        except Exception as e:
            # Display the error message in the text_loaded_output widget.
            self.display_in_output_text(f"Error: {type(e).__name__}.\n"
                                       "Error details: \n\n"
                                       f"{e}\n\n"
                                       "Please load a different file and try again.")
    
    def run(self):
        """Start the Tkinter event loop."""
        self.root.mainloop()