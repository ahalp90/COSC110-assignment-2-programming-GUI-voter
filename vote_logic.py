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


import copy # Used for dictionary deep copy
import os
import tkinter as tk
from tkinter import ttk
# candidate_votes_dict = {}

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
    
    # Create a candidate list without semicolons.
    ln1_candidates = ln1.split(";")
    
    # Check for excess semicolons, either as leading/trailing figures in the line or 
    # between candidate places. 
    # split(";") returns "" if there ";" in a string if there are multiple ";" 
    # or before/after a leading/trailing ";".
    for i in ln1_candidates:
        if i == (""):
            print("Error: Your list contains either a leading/trailing semicolon or "
                  "one or more candidate places contain >1 semicolons separating them.")
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
    # A list to store all the final cleaned votes, to avoid reiteration at dictionary processing.
    meta_cleaned_votes_list = []
    for line in lines_from_second: # Iterate through all vote lines (NB header was ln1).
        line_ints_list = [] # Create a local list to store the cleaned vote output of each line.

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
            except:
                print(f"Caught an error: {type.__name__}") # rewrite to include catching other errors.
                print("Error: A vote line likely contains either: (1) non-digit characters, (2) or "
                      "one or more votes contained >1 semicolons separating them."
                      "(3) a leading or trailing semicolon, or (4) an empty line.")
                return False

        # Check that each vote line's number of votes matches the number of candidates from the header.
        if len(line_ints_list) != quantity_of_candidates:
            print("Error: The number of candidates in your header line does not match "
                  "the votes in at least one vote line.")
            return False
        
        # Check that all candidates from header are represented as an index position within each vote.
        for candidate_number in range (1, quantity_of_candidates + 1):
            if candidate_number not in line_ints_list:
                print("Error: At least one vote does not represent all candidates from your header line.")
                return False # Exit and return false at the first candidate number not represented.
        
        # Add cleaned vote list to global vote list, so as not to reiterate at dictionary construction.
        meta_cleaned_votes_list.append(line_ints_list)

        # # Add votes to dictionary; according to instructions this should be a return value of load_file??
        # # Adding votes here is inefficient in the case of an invalid file discovered >1 line in,
        # # but it's more efficient than reiterating in the case of a valid file.
        # for key, vote in zip(candidate_votes_dict.keys(), line_ints_list):
        #     candidate_votes_dict[key] += vote
       
    print("Your votes are validly formatted and all candidates are represented.")
    return True, meta_cleaned_votes_list

def calculate_and_sort_borda_results(ln1_candidates, meta_cleaned_votes_list):
    n = len(ln1_candidates)
    final_tally = {candidate: 0 for candidate in ln1_candidates}

    try:
        for voteset in meta_cleaned_votes_list:
            for ranking, candidate in zip(voteset, final_tally.keys()):
                final_tally[candidate] += n - ranking
        print(f"{final_tally}")
    except:
        print("Error: An error occured when Borda tallying the final dictionary points.")
        return False
    print(f"{final_tally}")

    try:
        sorted_borda_dict = dict(sorted(final_tally.items(), key = lambda item: (-item[1], item[0])))
        print(f"{sorted_borda_dict}")
        return sorted_borda_dict
    except:
        print("Error: An error occured when applying the final sort to the candidate points dictionary.")
        return False
    


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
header_validation_result = valid_first_line(ln1)
if header_validation_result == False:
    print("Error: Exiting program due to an invalid header line in the input file.")
else:
    _, ln1_candidates = valid_first_line(ln1)
    # Populate dictionary with candidate keys in indexed order.
    for candidate in ln1_candidates:
        candidate_votes_dict[candidate] = 0

    votes_validation_result = check_votes_validity_and_add_to_dictionary(ln1_candidates, lines_from_second)
    if votes_validation_result == False:
        print("Error: Exiting program due to an invalidity in the vote lines of the input file.")
    else:
        print(candidate_votes_dict)