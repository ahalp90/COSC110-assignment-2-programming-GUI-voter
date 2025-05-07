import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def load_file(filename):
    try:
        with open(filename, 'r') as f:
            ln1 = f.readline().strip() # Read first line. Remove invisible chars like \n.
            # Return all voting lines. Strip invisible chars. Readlines starts at point readline() stopped.
            lines_from_second = [line.strip() for line in f.readlines()]
        
        ln1_candidates = valid_first_line(ln1)

        meta_cleaned_votes_list = check_votes_validity_and_export_to_list(ln1_candidates, lines_from_second)
        
        sorted_borda_dict = calculate_and_sort_borda_results(ln1_candidates, meta_cleaned_votes_list)
        
        return sorted_borda_dict
    
    # Identify and raise major likely errors to occur when accessing a file.
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {filename} could not be found.\n"
            "Please try again.")
    except PermissionError:
        raise PermissionError(f"Error: You don't have permission to access the file {filename}.\n"
            "Please try again.")
    except IOError as e:
        raise IOError(f"An IO error occured with file {filename}: {e}")

# Assumes that the only valid semi-colon placement in candidate listing is one semi-colon between candidates,
# and that trailing semicolons are never placed after the final candidate.
# Also checks that there is at least 1 candidate.
def valid_first_line (ln1):
    # Check that the candidate line is not empty.
    # This is technically redundant due to the later <if i == ("")> check.
    # However, it's more efficient to catch a bad file at the first likely error-point, 
    # and this is a simple check.
    if len(ln1) == 0:
        raise ValueError("Empty candidate line in input file.")
    
    # Create a candidate list without semicolons.
    ln1_candidates = ln1.split(";")
    
    # Check for excess semicolons, either as leading/trailing figures in the line or 
    # between candidate places. 
    # split(";") returns "" if there ";" in a string if there are multiple ";" 
    # or before/after a leading/trailing ";".
    if "" in ln1_candidates:
        raise ValueError("Candidate line contains (1) leading/trailing semicolon or\n"
                         "(2)multiple semicolons between candidates.")
    
    return ln1_candidates

# Check votes line-by-line for compliance with conditions.
# Checks are iterative (character/line-based) to efficiently stop at the first erroneous entry.
# Check that: 
# (1) The file has at least one line of votes.
# (2) All vote lines have only digits and semicolons.
# (3) Votes don't contain an excess leading/trailing semicolon.
# (4) Votes contain no excess semicolons between voting digits.
# (5) Votes are not blank lines.
# (6) vote lines have the same number of votes as candidates in the header, and 
# (7) vote lines contain numbers representing all candidates.
def check_votes_validity_and_export_to_list(ln1_candidates, lines_from_second):
    # Catch the situation where a file has no line after the header.
    if not lines_from_second:
        raise ValueError("Your file contains no voting lines; only a header")
    
    # Create a local variable to avoid recalculating at each iteration.
    quantity_of_candidates = len(ln1_candidates)
    # A list to store all the final cleaned votes, to avoid reiteration at dictionary processing.
    meta_cleaned_votes_list = []
    # Iterate through all vote lines (NB header was ln1).
    # enumerate() to return index position for user to identify erroneous line in file.
    for index_pos, line in enumerate(lines_from_second):
        line_ints_list = [] # Create a local list to store the cleaned vote output of each line.
        # Use for error returns. Gives the line number in a format that's intuitive to users;
        # Adds 2 to account for starting from the second line of the file and that [0] is first iteration.
        user_friendly_line_pos = index_pos + 2

        # Local list stores line votes as list stripped of semicolons.
        # Necessary intermediate to verify if there were incorrectly placed semicolons.
        line_without_semicolons_list = line.split(";")

        # Check that vote strings contain only digits or semicolons.
        # Implicitly includes check for >1 semicolon between votes and leading/trailing semicolons
        # ("" in stripped list).
        for i in line_without_semicolons_list:
            try:
                line_ints_list.append(int(i))
            except ValueError:
                raise ValueError(f"An error occured at line {user_friendly_line_pos} of your voting file.\n"
                                 "This vote line contains either: \n"
                                 "(1) non-digit characters, \n"
                                 "(2) one or more votes contained >1 semicolons separating them, \n"
                                 "(3) a leading or trailing semicolon, or \n"
                                 "(4) an empty line.")


        # Check that each vote line's number of votes matches the number of candidates from the header.
        if len(line_ints_list) != quantity_of_candidates:
            raise ValueError("The number of candidates in your header line does not match "
                             "the number of votes in at least one vote line.\n"
                             f"This error first occured in line {user_friendly_line_pos} of your voting file.")
        
        # Check that all candidates from header are represented as an index position within each vote.
        for candidate_number in range (1, quantity_of_candidates + 1):
            if candidate_number not in line_ints_list:
                raise ValueError("At least one vote does not represent all candidates from your header line. \n"
                                 f"This error first occured in line {user_friendly_line_pos} of your voting file.")
        
        # Add cleaned vote list to a vote list and return this so as not to reiterate at dictionary construction.
        meta_cleaned_votes_list.append(line_ints_list)
      
    return meta_cleaned_votes_list

def calculate_and_sort_borda_results(ln1_candidates, meta_cleaned_votes_list):
    """Calculate election results using the Borda Count formula and then sort them.

    Create an intermediate dictionary (final_tally) of all candidates with value 0. 
        Iterate through the passed in list of clean votes (a meta list containing 
        each vote line as a sub-list) and the local dictionary of candidates. 
        Derive a vote value from each index position's integer within each voteset 
        and pair it to the correlated position of the vote_tally dictionary keys.
        Process the votes according to the given formula and then iteratively 
        add to the keys' values in final_tally.

    For each vote, candidates receive points based on their rankings.
        Each candidate earns (n - r) points for each ballot, where:
        n = Total number of candidates (3 in this case)
        r = Rank assigned by the voter
        In this case:
        A 1st place vote gives the candidate 2 points (3 - 1)
        A 2nd place vote gives 1 point (3 - 2)
        A 3rd place vote gives 0 points (3 - 3)
    
    Subsequently, sort the keys according to the given criteria.
        Keys should be sorted in descending order of value, and
        in the case of a tied value, an alphabetical sort should be applied.
  
    Arguments:
        ln1_candidates (list): List of candidate names with semicolons removed.
        meta_cleaned_votes_list (list): List containing child lists with each line
            of votes, with semicolons removed.

    Returns:
        sorted_borda_dict dict: A dictionary mapping each candidate to their
        total Borda Count points and sorted by descending value order and,
        in the case of a tied value, in alphabetical order.

    Raises:
        ValueError: Unforseen run-time issues may impact dictioanry construction
            or sorting. Raise these as ValueError messages but preserve the originating
            error code.
    """
    # Local variable to avoid recalculating the number of candidates 
    n = len(ln1_candidates)
    # Local dictionary to store candidates (keys) and their values while tallying
    # and sorting.
    final_tally = {candidate: 0 for candidate in ln1_candidates}

    # Tally votes for each candidate using the Borda algorithm.
    try:
        for voteset in meta_cleaned_votes_list:
            for ranking, candidate in zip(voteset, final_tally.keys()):
                final_tally[candidate] += n - ranking
    
    # Handle unanticipated calculation errors when tallying dictionary points, 
    # but pointing to the specific error-type.
    except Exception as e:
        raise ValueError(f"An error occured when Borda tallying the final dictionary points: {e}")

    # Create and return a dictionary derived from the local vote_tally dictionary
    # with requisite sort applied.
    try:
        sorted_borda_dict = dict(sorted(final_tally.items(), key = lambda item: (-item[1], item[0])))
        return sorted_borda_dict
    
    # Handle unanticipated computation errors when sorting the dictionary, 
    # but pointing to the specific error-type.
    except Exception as e:
        raise ValueError("An error occured when applying the final sort "
                         f"to the candidate points dictionary: {e}")
    
## GUI Logic
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
                                    "Click the 'Find my file' button to navigate to your file "
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

# Momentarily set the output textbox to normal, delete all text from the first line to the end,
# insert the desired text and then render it read-only again.
def display_in_output_text(message_text):
    text_loaded_output.config(state=tk.NORMAL)
    text_loaded_output.delete('1.0', tk.END)
    text_loaded_output.insert(tk.END, message_text)
    text_loaded_output.config(state=tk.DISABLED)

# Call file dialog window with appropriate title and file-type restrictions.
# Set the text of label_file_selected based on the file selected;
# strip the path on the text for non-technical users.
# Return file_path
def open_file_dialog():
     # Clear output text each time there's an attempt to load a new file; 
     # assumes >1 attempt, probably after loading a failed file.
    display_in_output_text(message_text="")

    filename = filedialog.askopenfilename(title="Select a File", 
                                           filetypes=[("Text files", "*.txt"), 
                                                      ("All files", "*.*")])
    if filename:
        selected_file_path.set(filename)
        label_file_selected.config(text=f"File selected: {os.path.basename(filename)}")


def handle_load_file_click():
    filename = selected_file_path.get()
    
    try:
        sorted_borda_dict = load_file(filename)
        
        output_list = []
        for candidate, score in sorted_borda_dict.items():
            output_list.append(f"{candidate}: {score}")
        
        output_message =  (f"Sucessfully loaded and processed: {os.path.basename(filename)}\n\n"
                            "Borda Count Results of the Codetown Election\n\n"
                            "Candidate: Score\n\n"
                            f"{"\n".join(output_list)}")
        display_in_output_text(output_message)
    
    except Exception as e:
        display_in_output_text(f"Error: {type(e).__name__}.\n"
                               "Error details: \n\n"
                               f"{e}\n\n"
                               "Please load a different file and try again.")
        
# Widget bindings
button_file_finder.config(command=open_file_dialog)
button_file_load.config(command=handle_load_file_click)

root.mainloop()