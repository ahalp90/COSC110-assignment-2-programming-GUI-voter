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
candidate_votes_dict = {}

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
            # print(ln1, lines_from_second) # Debug helper
            return ln1, lines_from_second
    except FileNotFoundError as e:
        print(f"Error: {type(e).__name__}. {e}.\n"
                f"The file could not be found. Please try again.")
        return None, None
    except PermissionError as e:
        print(f"Error: {type(e).__name__}. {e}.\n"
                f"You don't have permission to access this file.\n"
                f"Please try again.")
        return None, None
    except Exception as e: # General error catcher
        print(f"Error: {type(e).__name__}. Error details: {e}")
        return None, None

# Assumes that the only valid semi-colon placement in candidate listing is one semi-colon between candidates,
# and that trailing semicolons are never placed after the final candidate.
# Also checks that there is at least 1 candidate.
def valid_first_line (ln1):
    # Check that the candidate line is not empty.
    # This is technically redundant due to the later <if i == ("")> check.
    # However, it's more efficient to catch a bad file at the first likely error-point, 
    # and this is a simple check.
    if len(ln1) == 0:
        print("Error: Empty candidate line in input file.")
        return False
    
    # Check that semicolons appropriately separate candidates
    # Check that there are no leading/trailing semicolons
    for char in ln1:
        if char([0] or [-1]) == (";"):
            print("Error: Your candidate list contains an excess semicolon at its start or finish.")
            return False
    # Create a candidate list without semicolons.
    ln1_candidates = ln1.split(";")
    # Check for excess semicolons between candidate places, 
    # as split at ";;" returns an empty string at the index position ("").
    for i in ln1_candidates:
        if i == (""):
            print("Error: One or more candidate places contained >1 semicolons separating them.")
            return False
    
    # Check for leading/trailing whitespace between candidate names and semicolons.
    # Assumes that a candidate name that starts/ends with a whitespace would be invalid.
    for i in ln1_candidates:
        if i([0] or [-1]) == (" "):
            print("Error: One more more candidate names begins/ends with whitespace. "
                  "This is against formatting conventions. Candidate names should only be "
                  "separated by a semicolon.")
            return False
    
    print("Your candidate line is appropriately formatted.")
    return True, ln1_candidates

# Check votes line-by-line for compliance with conditions.
# Checks are iterative (character/line-based) to efficiently stop at the first erroneous entry.
# Check that: 
# (1) Votes don't contain an excess leading/trailing semicolon,
# (2) all vote lines have only digits and semicolons, 
# (3) votes contain no excess semicolons between voting digits,
# (4) vote lines have the same number of votes as candidates in the header, and 
# (5) vote lines contain numbers representing all candidates.
def check_votes_validity_and_add_to_dictionary(ln1_candidates, lines_from_second):
    # Create a local variable to avoid recalculating at each iteration.
    quantity_of_candidates = len(ln1_candidates)
    for line in lines_from_second: # Iterate through all vote lines (NB header was ln1).
        # Check that the vote line is not empty.
        # This is technically redundant due to the later check that the number of vote positions == the number of candidates.
        # However, it's more efficient to catch a bad file at the first likely error-point, 
        # and this is a simple check.
        if len(line) == 0:
            print("Error: Empty vote line in input file.")
            return False
        
        line_votes_list = [] # Create a local list to store each line's clean votes.
        line_semicolon_count = 0 # Create a local list to store each line's semicolon count.
        
        # Check there's no excess leading/trailing semicolon.
        if line([0] or [-1]) == (";"):
            print("Error: A vote line contains an excess semicolon at its start or finish.")
            return False
        for char in line: # Check each character individually.
            # Return an error if a character is not a semicolon or a digit.
            # TODO: Redundant if i'm trying to convert to int type
            # DELETE
            if not (char == ";" or char.isdigit()):
                print("Error: Characters are not ; or digits.")
                return False # Exit and return false at the first incorrect character.
            
        # Local parent lists take strips semicolons and takes each vote as a list place.
        for char in line:
            try:
                if (";"):
                    line_semicolon_count += 1
                else :
                    char = char(int)
                    line_votes_list.append(char)
            except:
                print("A vote line contains a non-allowed character (not semicolon or digit).")
        
        if len(line_votes_list) != line_semicolon_count +1
            print("Your line contai")
            return False
        for i in line_digits_list:
            try:
                
            if i == "":
                print("Error: One or more votes contained >1 semicolons separating them.")
                return False

        # Check that each vote line's number of votes matches the number of candidates from the header.
        if len(line_digits_list) != quantity_of_candidates:
            return False
        
        # Check that all candidates from header are represented as an index position within each vote.
        for candidate_number in range (1, quantity_of_candidates + 1):
            if candidate_number not in line_digits_list:
                print("The vote numbers don't line up with the number of candidates.")
                return False # Exit and return false at the first candidate number not represented.
        
        # Add votes to dictionary; according to instructions this should be a return value of load_file??
        # Adding votes here is inefficient in the case of an invalid file discovered >1 line in,
        # but it's more efficient than reiterating in the case of a valid file.
        for key, vote in zip(candidate_votes_dict.keys(), line_digits_list):
            candidate_votes_dict[key] += vote
       
    print("Your votes are validly formatted and all candidates are represented.")
    return True

def results_sort_and_borda_count():
    pass
    # Borda count


# Run code
while True:
    open_folder()
    filename = get_filename() # Executable line here to store filename
    ln1, lines_from_second = load_file(filename) # Executable line to store ln1 and lines_from_second values and unpack return tuple.
    if ln1 and lines_from_second is not (None, None):
        print(f"Successfully loaded data from {filename}")
        break
    print("Please try entering the filename again.")
# Check candidate line for validity.
# Get list of candidates stripped of semicolons.
# Throw away the boolean part of the valid_first_line(ln1) return.
_, ln1_candidates = valid_first_line(ln1)

# Populate dictionary with candidate keys in indexed order.
for candidate in ln1_candidates:
    candidate_votes_dict[candidate] = 0

check_votes_validity_and_add_to_dictionary(ln1_candidates, lines_from_second)
print(candidate_votes_dict)

# fix check for numbers > candidate_quantity
# 