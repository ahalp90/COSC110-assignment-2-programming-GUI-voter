# Check first line first.
    # with open("demofile.txt") as f:
    #   print(f.readline()) 


# counter info https://docs.python.org/3/library/collections.html#collections.Counter
# Import OS to get file directory and os methods.

# def open_folder_with_dir_tree():
#     cwd = os.getcwd()
#     path = cwd
#     list = []

#     for (root, dirs, files) in os.walk(path):
#         for f in files:
#             if f.endswith(".txt"):
#                 print(f"{root}/{f}")


import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# List txt files in the directory.
def open_folder():
    cwd = os.getcwd() # Redundant (and redundant param in method call).
    for x in os.listdir(cwd):
        if x.endswith(".txt"):
            print(x)


def get_filename():
    filename = input("Please enter the name of the file to open: ")
    return filename



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
    
    # Call here the raised ValueError exceptions originating within the try loop's called functions.
    except ValueError as e:
        raise e


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
        raise ValueError("Candidate line contains leading/trailing semicolon "
                         "or multiple semicolons between candidates.")
    
    return ln1_candidates

# Check votes line-by-line for compliance with conditions.
# Checks are iterative (character/line-based) to efficiently stop at the first erroneous entry.
# Check that: 
# (1) Votes don't contain an excess leading/trailing semicolon,
# (2) all vote lines have only digits and semicolons, 
# (3) votes contain no excess semicolons between voting digits,
# (4) vote lines have the same number of votes as candidates in the header, and 
# (5) vote lines contain numbers representing all candidates.
def check_votes_validity_and_export_to_list(ln1_candidates, lines_from_second):
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
        print("Removing semicolons from vote line.")

        # Check that vote strings contain only digits or semicolons.
        # Implicitly includes check for >1 semicolon between votes and leading/trailing semicolons
        # ("" in stripped list).
        for i in line_without_semicolons_list:
            try:
                line_ints_list.append(int(i))
            except ValueError:
                raise ValueError(f"An error occured at line {user_friendly_line_pos} of your voting file. "
                                 "This vote line contains either: (1) non-digit characters, "
                                    "(2) one or more votes contained >1 semicolons separating them, "
                                    "(3) a leading or trailing semicolon, or (4) an empty line.")


        # Check that each vote line's number of votes matches the number of candidates from the header.
        if len(line_ints_list) != quantity_of_candidates:
            raise ValueError("The number of candidates in your header line does not match "
                             "the votes in at least one vote line."
                             f"This error first occured in line {user_friendly_line_pos} of your voting file.")
        
        # Check that all candidates from header are represented as an index position within each vote.
        for candidate_number in range (1, quantity_of_candidates + 1):
            if candidate_number not in line_ints_list:
                raise ValueError("At least one vote does not represent all candidates from your header line. "
                                 f"This error first occured in line {user_friendly_line_pos} of your voting file.")
        
        # Add cleaned vote list to a vote list and return this so as not to reiterate at dictionary construction.
        meta_cleaned_votes_list.append(line_ints_list)
      
    print("Your votes are validly formatted and all candidates are represented.")
    return meta_cleaned_votes_list

def calculate_and_sort_borda_results(ln1_candidates, meta_cleaned_votes_list):
    n = len(ln1_candidates)
    final_tally = {candidate: 0 for candidate in ln1_candidates}

    try:
        for voteset in meta_cleaned_votes_list:
            for ranking, candidate in zip(voteset, final_tally.keys()):
                final_tally[candidate] += n - ranking
    # Handle unanticipated calculation errors when tallying dictionary points, 
    # but pointing to the specific step in the code.
    except Exception as e:
        raise ValueError(f"An error occured when Borda tallying the final dictionary points: {e}")

    try:
        sorted_borda_dict = dict(sorted(final_tally.items(), key = lambda item: (-item[1], item[0])))
        return sorted_borda_dict
    # Handle unanticipated computation errors when sorting the dictionary, 
    # but pointing to the specific step in the code.
    except Exception as e:
        raise ValueError(f"An error occured when applying the final sort "
                         "to the candidate points dictionary: {e}")
    
# Function to print sorted and tallied borda count dictionary.
def print_sorted_results(sorted_borda_dict):
    print(f"{sorted_borda_dict}")

# Run code
while True:
    open_folder()
    filename = get_filename() # Executable line here to store filename
    try:
        sorted_borda_dict = load_file(filename)
        print(f"Successfully loaded file from {filename}")
        print_sorted_results(sorted_borda_dict)
        break
    except FileNotFoundError:
        print(f"The file {filename} could not be found.\n"
                f"Please try again.")
    except PermissionError:
        print(f"Error: You don't have permission to access the file {filename}.\n"
                f"Please try again.")
    except Exception as e: # General error catcher for unforeseen circumstances.
        print(f"An unexpected error occured. Please try again.\n"
                f"Error: {type(e).__name__}. Error details: {e}.")
        

