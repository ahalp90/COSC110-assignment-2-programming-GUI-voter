"""
Codetown Vote Display

This program processes files containg election data to calculate and display 
    results using the Borda Count method. Its interface is configured by default
    to expect files in <.txt> format.
It features a GUI built with Tkinter for file selection and display of results 
    or error messages.
Loaded vote files are checked for validity. A valid vote file will prompt the 
    generation of a borda-counted dictionary of candidates and their points 
    allocated. This dictionary is sorted (Python 3.7+) by descending key value, 
    and in the event of a tied-value, alphabetical order at that value.

Input files must meet the following conditions:
1. The first line is a semicolon-separated string of candidate names.

2. Subsequent lines are semicolon-separated strings of numerical (integer) 
    rankings. Each line is understood to be a single voter's voteset for the 
    candidates in the header. Each voteset must rank all candidates, and contain
    the same number of rankings as number of candidate positions in the header 
    line.

3. The order of values in each line is expected to be:
    3.1 Header: candidatename - semicolon- candidatename
    3.2 Voteset lines: vote integer(s) - semicolon - vote integer(s)

Any line that does not meet these conditions will be treated as invalid and 
    trigger an error message, displayed in the GUI.

A valid file that has been successfully Borda-counted and sorted will produce 
    a tally of candidate points in the GUI.
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def load_file(filename):
    """
    Loads, validates and processes a vote data file.

    This function calls a series of child functions to achieve the following:
    1. Read the file referred by <handle_load_file_click>.
    2. Produce variables containing (1) the header line and (2) all subsequent 
        voteset lines.
    3. Validate the contents of the voting file.
    4. Produce a dictionary of counted and sorted results.

    Arguments:
        filename (string): The path to the election data file.

    Returns:
        sorted_borda_dict (dict): A dictionary mapping each candidate to their
            total Borda Count points and sorted by descending value order and,
            in the case of a tied value, in alphabetical order.

    Raises:
        FileNotFoundError: If the file to load does not exist.
        PermissionError: If the program does not have permission to read the 
            file.
        IOError: For other IO errors during file access.
        ValueError: Specific errors raised from child functions concerning 
            vote file content validity or dictionary compilation.
    """
    try:
        # Read first line. Remove leading/trailing invisible chars like \n.
        with open(filename, 'r') as f:
            ln1 = f.readline().strip()
            # Return all voting lines. Strip invisible leading/trailing chars. 
            # readlines() starts at the point readline() stopped within the 
            # calling function.
            lines_from_second = [line.strip() for line in f.readlines()]
        
        # Validate the candidate line and extract candidate names to a list.
        ln1_candidates = valid_first_line(ln1)

        # Validate vote lines and convert them to a single list of 
        # voteset integer lists.
        meta_cleaned_votes_list = check_votes_validity_and_export_to_list(
            ln1_candidates, lines_from_second)
        
        # Borda-calculate and sort a dictionary from the results.
        sorted_borda_dict = calculate_and_sort_borda_results(
            ln1_candidates, meta_cleaned_votes_list)
        
        return sorted_borda_dict
    
    # Identify and raise major likely errors to occur when accessing a file.
    # Provide user-friendly error messages.
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {filename} could not be found.\n"
            "Please try again.")
    except PermissionError:
        raise PermissionError(
            f"Error: You don't have permission to access the file {filename}.\n"
            "Please try again.")
    # Catch other unforeseen IO errors.
    except IOError as e:
        raise IOError(f"An IO error occured with file {filename}: {e}")

def valid_first_line (ln1):
    """
    Validates the first line (candidate names) of the file loaded.

    Checks:
    (1) The line is not empty.
    (2) There are no leading/trailing semicolons.
    (3) There are no multiple semicolons between candidate names.
    (4) There is at least one candidate.

    Arguments:
        ln1 (string): The first line read from the file loaded.
    
    Returns:
        ln1_candidates (list): A list of candidate names.
    
    Raises:
        ValueError: If the candidate line is invalid.
    """
    # Check that the candidate line is not empty.
    # Technically redundant due to the later <if i == ("")> check.
    # However, most efficient to catch a bad file at the first likely error.
    if len(ln1) == 0:
        raise ValueError("Empty candidate line in input file.")
    
    # Create a candidate list without semicolons of candidate name strings.
    ln1_candidates = ln1.split(";")
    
    # Check for excess semicolons, either as leading/trailing figures in the 
    # line or between candidate places. 
    # split(";") returns "" (an empty string) if there are multiple consecutive
    # semicolons or if the original input string contained a 
    # leading/trailing ";".
    if "" in ln1_candidates:
        raise ValueError("Candidate line contains (1) leading/trailing semicolon or\n"
                         "(2)multiple semicolons between candidates.")
    
    return ln1_candidates


def check_votes_validity_and_export_to_list(ln1_candidates, lines_from_second):
    """
    Validates vote lines and converts them into a list of lists of integers.

    Check votes line-by-line for compliance with conditions.
    Checks are iterative (character/line-based) to efficiently stop at the first
        erroneous entry.
    Check that: 
        (1) The file has at least one line of votes.
        (2) All vote lines have only digits and semicolons.
        (3) Votes don't contain an excess leading/trailing semicolon.
        (4) Votes contain no excess semicolons between voting digits.
        (5) Votes are not blank lines.
        (6) Vote lines have the same number of votes as candidates in the header. 
        (7) Vote lines contain numbers representing all candidates.

    Arguments:
        ln1_candidates (list): A list of candidate names.
        lines_from_second (list): A list of all voting lines, passed locally 
            within load_file(filename) 
    
    Returns:
        meta_cleaned_votes_list (list): A list of lists containing votesets of 
            integer ranks.
    
    Raises:
        ValueError: Specific error message for why a vote line was invalid.
    """
    # Catch the situation where a file has no line after the header.
    if not lines_from_second:
        raise ValueError("Your file contains no voting lines; only a header")
    
    # Local variable avoids recalculating at each iteration.
    quantity_of_candidates = len(ln1_candidates)
    # List to store all the final cleaned votes; avoid reiteration at 
    # dictionary processing.
    meta_cleaned_votes_list = []
    # Iterate through all vote lines to validate (NB. header was ln1).
    # enumerate() to return index position for user to identify erroneous line 
    # in file.
    for index_pos, line in enumerate(lines_from_second):
        # Local list stores the cleaned vote output of each line.
        line_ints_list = []
        # Use for error returns. User friendly numbering: +2 accounts for 
        # starting from the 2nd line of the loaded file (index_pos [0]).
        user_friendly_line_pos = index_pos + 2

        # Local list of line's vote characters stripped of semicolons.
        # Necessary intermediate to verify incorrectly placed semicolons.
        line_without_semicolons_list = line.split(";")

        # Check that vote strings contain only digits 
        # (or, implicitly based on the above split, previously only digits and 
        # semicolons).
        # Implicitly includes check for >1 semicolon between votes, 
        # leading/trailing semicolons ("" in stripped list) and empty lines.
        for i in line_without_semicolons_list:
            try:
                line_ints_list.append(int(i))
            except ValueError:
                raise ValueError(
                    f"An error occured at line {user_friendly_line_pos} of your "
                    "voting file.\n"
                    "This vote line contains either: \n"
                    "(1) non-digit characters, \n"
                    "(2) one or more votes contained >1 semicolons separating "
                    "them, \n"
                    "(3) a leading or trailing semicolon, or \n"
                    "(4) an empty line.")


        # Check that each vote line's number of votes matches the number of 
        # candidates from the header.
        if len(line_ints_list) != quantity_of_candidates:
            raise ValueError(
                "The number of candidates in your header line does not match "
                "the number of votes in at least one vote line.\n"
                f"This error first occured in line {user_friendly_line_pos} of "
                "your voting file.")
        
        # Check that all candidates from header are represented as an index 
        # position within each vote.
        # This combined with the previous check also ensures that all vote 
        # rankings are unique per line.
        for candidate_number in range (1, quantity_of_candidates + 1):
            if candidate_number not in line_ints_list:
                raise ValueError(
                    "At least one vote does not represent all candidates from "
                    "your header line. \n"
                    f"This error first occured in line {user_friendly_line_pos} "
                    "of your voting file.")
        
        # If all checks pass, add cleaned the line's vote list to a list-of-lists.
        # Return this afterward to not reiterate at dictionary construction.
        meta_cleaned_votes_list.append(line_ints_list)
      
    return meta_cleaned_votes_list

def calculate_and_sort_borda_results(ln1_candidates, meta_cleaned_votes_list):
    """
    Calculate election results using the Borda Count formula and sort them.

    Create an intermediate dictionary (final_tally) of all candidates with 
        value 0. 
        Iterate through the passed in list of clean votes (a meta list containing 
        each vote line as a sub-list) and the local dictionary of candidates. 
        Derive a vote value from each index position's integer within each voteset 
        and pair it to the correlated position of the vote_tally dictionary keys.
        Process the votes according to the given formula and then iteratively 
        add to the keys' values in final_tally.

    For each vote, candidates receive points based on their rankings.
        Each candidate earns (n - r) points for each ballot, where:
        n = Total number of candidates
        r = Rank assigned by the voter
        For example, with three candidates:
        A 1st place vote gives the candidate 2 points (3 - 1)
        A 2nd place vote gives 1 point (3 - 2)
        A 3rd place vote gives 0 points (3 - 3)
    
    Subsequently, sort the keys according to the given criteria.
        Keys should be sorted in descending order of value, and
        in the case of a tied value, an alphabetical sort should be applied.
  
    Arguments:
        ln1_candidates (list): List of candidate names with semicolons removed.
        meta_cleaned_votes_list (list): List containing child lists with each 
            line of votes, with semicolons removed.
            Order within each list corresponds to the order of candidates in 
            ln1_candidates.

    Returns:
        sorted_borda_dict (dict): A dictionary mapping each candidate to their
        total Borda Count points and sorted by descending value order and,
        in the case of a tied value, in alphabetical order.

    Raises:
        ValueError: Unforseen run-time issues may impact dictionary construction
            or sorting. Raise these as ValueError messages but preserve the 
            originating error code.
    """
    # Local variable avoids recalculating the number of candidates at iteration.
    n = len(ln1_candidates)
    # Local dictionary to store candidates (keys) and their values while 
    # tallying and sorting.
    final_tally = {candidate: 0 for candidate in ln1_candidates}

    # Tally votes for each candidate using the Borda algorithm.
    try:
        # Iterate through each voteset list.
        for voteset in meta_cleaned_votes_list:
            # Iterate simultaneously through voteset index positions and 
            # candidate keys.
            for ranking, candidate in zip(voteset, final_tally.keys()):
                # Apply the borda count to each key's value and increment it 
                # appropriately each iteration.
                final_tally[candidate] += n - ranking
    
    # Handle unanticipated calculation errors when tallying dictionary points, 
    # but pointing to the specific error-type.
    except Exception as e:
        raise ValueError(
            "An error occured when Borda tallying the final dictionary "
            f"points: {e}")

    # Create and return a dictionary derived from the local vote_tally 
    # dictionary with requisite sort applied.
    # Primary sort: descending point value. 
    # Secondary sort: ascending alphabetical.
    try:
        sorted_borda_dict = dict(
            sorted(final_tally.items(), key = lambda item: (-item[1], item[0])))
        return sorted_borda_dict
    
    # Handle unanticipated computation errors when sorting the dictionary, 
    # but pointing to the specific error-type.
    except Exception as e:
        raise ValueError("An error occured when applying the final sort "
                         f"to the candidate points dictionary: {e}")
    
#-------------------------------------------------------------------------------
# GUI Logic
#
# Frames:
# (1) root
# (2) frame_loading
# (3) frame_load_output
# (4) header
#
# Widgets:
#   label_header
#   label_instructions
#   button_file_finder
#   button_file_load
#   label_file_selected
#   text_loaded_output
#   scrollbar_y
#-------------------------------------------------------------------------------
# Initialise the main Tkinter window.
root = tk.Tk()
root.title("Codetown Vote Counter")
root.minsize(800,500) # Minimum window size; not strictly enforced in Linux.

#Tkinter StringVar to hold the path of the selected file.
#tk.StringVar() type in case of later use for direct read/write by tk objects.
selected_file_path = tk.StringVar()

# Create layout frames.
frame_loading = ttk.Frame(root)
frame_load_output = ttk.Frame(root)

# WIDGETS.
# Main header.
# Header in root to avoid replication if additional frames are added in an update.
label_header = ttk.Label(root, 
                         text="Codetown Vote Display",
                         anchor='center',
                         font='bold')

# Loading frame widgets.
label_instructions = ttk.Label(
    frame_loading, 
    text="Please select a file to load.\n\n"
    "Click the 'Find my file' button to navigate to your file "
    "in its directory.\n\n"
    "Once you're satisfied with your file chosen, press the 'Load file' button.", 
    wraplength=700, # Wrap to frame minwidth minus a bit of buffer.
    justify=tk.LEFT)
button_file_finder = ttk.Button(frame_loading, 
                                text="Find my file")
button_file_load = ttk.Button(frame_loading, 
                              text="Load file")
label_file_selected = ttk.Label(
    frame_loading, 
    text="No file currently selected", 
    wraplength=700, # Wrap to frame minwidth minus a bit of buffer.
    anchor='w')

# Output display frame widgets (frame_load_output).
# Text widget displays vote count/error messages, and y scrollbar for it.
text_loaded_output = tk.Text(frame_load_output, 
                              height=10, 
                              borderwidth=1, 
                              relief=tk.FLAT, 
                              bg='white', 
                              state=tk.DISABLED,  #Initially read-only.
                              wrap=tk.WORD)

# Vertical scrollbar for the text_loaded_output widget.
scrollbar_y = ttk.Scrollbar(
    frame_load_output, orient=tk.VERTICAL, command=text_loaded_output.yview)

# Configure the Text widget to use the scrollbar.
text_loaded_output.config(yscrollcommand=scrollbar_y.set)

# Configure frame borders for frame_loading and frame_load_output.
frame_loading.configure(padding=5, borderwidth=2)
frame_load_output.configure(padding=5)

# GRID LAYOUT FOR WIDGETS.
# Root widgets.
# <label_header> is in a separate grid in case of refactoring for additional frames.
label_header.grid(column=0, row=0, pady=(10, 10), sticky='ew')
frame_loading.grid(column=0, row=1, sticky='nsew')
frame_load_output.grid(column=0, row=2, columnspan=5, sticky='nsew')

# frame_loading widgets.
label_instructions.grid(column=0, 
                        row=0, 
                        columnspan=5, 
                        rowspan=1, 
                        pady=(0,30), 
                        sticky='nsew')
label_file_selected.grid(column=0, 
                         row=2, 
                         columnspan=4, 
                         rowspan=1, 
                         pady=(10,10), 
                         sticky='nsew')
button_file_finder.grid(column=4, 
                        row=1, 
                        columnspan=1, 
                        rowspan=1, 
                        pady=(5,5), 
                        sticky='nsew')
button_file_load.grid(column=4, 
                      row=2, 
                      columnspan=1, 
                      rowspan=1, 
                      pady=(5,5), 
                      sticky='nsew')

# frame_load_output widgets (Text and Scrollbar).
text_loaded_output.grid(column=0, 
                        row=0, 
                        sticky='nsew')
scrollbar_y.grid(column=1, 
                 row=0, 
                 columnspan=1, 
                 rowspan=3, 
                 sticky='ns')


# FRAME RESIZING BEHAVIOUR
# Resize properties for <Root> widgets
 # Root needs to expand as the container for all frames.
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=0) # Header doesn't expand.
root.rowconfigure(1, weight=1) # Main body frame expands.
root.rowconfigure(2, weight=1) # Output text frame expands.

# Resize properties for <frame_loading> widgets.
# Iterative due to facilitate ongoing UI tinkering
# Must call before using grid_size() value-check.
frame_loading.update_idletasks()
# Iterate through frame columns and rows to set weight=1, 
# All columns expand equally.
for i in range(frame_loading.grid_size()[0]):
    frame_loading.columnconfigure(i, weight=1)
# All rows expand equally.
for i in range(frame_loading.grid_size()[1]):
    frame_loading.rowconfigure(i, weight=1)

# Resize properties for output text frame.
# Text widget's column and row expand equally.
frame_load_output.columnconfigure(0, weight=1)
frame_load_output.rowconfigure(0, weight=1)


def display_in_output_text(message_text):
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
    text_loaded_output.config(state=tk.NORMAL)
    text_loaded_output.delete('1.0', tk.END)
    text_loaded_output.insert(tk.END, message_text)
    text_loaded_output.config(state=tk.DISABLED)

# Call file dialog window with appropriate title and file-type restrictions.
# Set the text of label_file_selected based on the file selected;
# strip the path on the text for non-technical users.
# Return file_path
def open_file_dialog():
    """
    Opens a file dialogue for the user to select an input file.

    Updates the 'selected_file_path' StringVar and the 'label_file_selected'
        widget with the chosen file's path.
    Only the basename--filename and filetype stripped of directory--is 
        displayed. This is for brevity and user-friendliness.
    Clears the output text area on a new file selection attempt.
    """
     # Clear output text each time there's an attempt to load a new file; 
     # assumes >1 attempt, probably after loading a failed file.
    display_in_output_text(message_text="")

    # Open file system dialogue, defaulting to only show <.txt> files.
    filename = filedialog.askopenfilename(title="Select a File", 
                                           filetypes=[("Text files", "*.txt"), 
                                                      ("All files", "*.*")])
    if filename: # If a file was selected to open.
        selected_file_path.set(filename)
        label_file_selected.config(
            text=f"File selected: {os.path.basename(filename)}")


def handle_load_file_click():
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
    filename = selected_file_path.get()
    
    # Handle the case that a file load is attempted before a file is selected.
    # Prints to screen rather than raising an exception as this is normal 
    # program operation behaviour.
    if not filename:
        display_in_output_text(
            "You've tried to load a file but haven't yet selected one to load.\n\n"
            "Please select a file using 'Find my file'.")
        return
    
    try:
        # Call load_file(filename) and assign the output to a variable.
        sorted_borda_dict = load_file(filename)
        
        # Format the election results dictionary for line-by-line display.
        output_list = []
        
        for candidate, score in sorted_borda_dict.items():
            output_list.append(f"{candidate}: {score}")
        
        output_message =  (
            f"Sucessfully loaded and processed: {os.path.basename(filename)}\n\n"
            "Borda Count Results of the Codetown Election\n\n"
            "Candidate: Score\n\n"
            # Print the lists's string values as successive on-screen lines.
            f"{"\n".join(output_list)}")
        
        display_in_output_text(output_message)
    
    # Receive all raised exceptions from child functions, as well as any 
    # unexpected exception originating here.
    except Exception as e:
        # Display the error message in the text_loaded_output widget.
        display_in_output_text(f"Error: {type(e).__name__}.\n"
                               "Error details: \n\n"
                               f"{e}\n\n"
                               "Please load a different file and try again.")
        
# WIDGET BINDINGS
# Connect button clicks to their associated functions.
button_file_finder.config(command=open_file_dialog)
button_file_load.config(command=handle_load_file_click)

# Start the Tkinter event loop.
root.mainloop()