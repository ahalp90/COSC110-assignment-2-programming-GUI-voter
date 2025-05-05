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
def valid_first_line (ln1, quantity_of_candidates):
    semicolons_in_ln1 = ln1.count(";")
    if quantity_of_candidates == 0:
        print("Error: No candidates in input file.")
        return False
    # Return an error where there's 
    elif semicolons_in_ln1 >= quantity_of_candidates:
        print("Error: Candidates not appropriately separated by semicolons in input file.")
        return False
    else:
        print("Your candidate line is appropriately formatted.")
        return True

# Check that (1) all vote lines have digits and semicolons, and (2) contain numbers representing all candidates.
# Does not verify that all vote numbers are distinct within a line. 
# That would require a cross-reference with a set/frozen set
def check_votes_validity_and_add_to_dictionary(lines_from_second, quantity_of_candidates):
    for line in lines_from_second: # Check all lines individually from second.
        line_digits_list = [] # Create a local list to store each line's digits.
        for char in line: # Check each character individually.
            # This could be reframed as a positive <if char == ;: continue> statement,
            # removing the duplicate isdigit() check.
            # However, this would make error-identification less informative.
            if not (char == ";" or char.isdigit()):
                print("Error: Characters are not ; or digits.")
                return False # Exit and return false at the first incorrect character.
            elif char.isdigit():
                char = int(char)
                # Check that all vote numbers correspond to a valid candidate place.
                if not 1<= char <= quantity_of_candidates:
                    print("Error: A vote falls outside the candidate range.")
                    return False # Exit and return false at the first incorrect character.
                # Append valid vote numbers, stripped of semicolons, to a local parent list.
                else:
                    line_digits_list.append(char)
                    print("Appending digits to list.")
        # Check that all candidates from header are represented as an index position within each vote.
        # Perform the check line-by-line to stop at the first indicator of an invalid file.
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

def results_sort():
    pass

class GUI:
    pass




# Run code
while True:
    open_folder()
    filename = get_filename() # Executable line here to store filename
    ln1, lines_from_second = load_file(filename) # Executable line to store ln1 and lines_from_second values and unpack return tuple.
    if ln1 and lines_from_second is not (None, None):
        print(f"Successfully loaded data from {filename}")
        break
    print("Please try entering the filename again.")
# Get list and quantity of candidates; could this be better moved into a precedent function?
candidate_list = list(ln1.split(";")) # Get list of candidates - name characters only.
quantity_of_candidates = len(candidate_list) # Store variable to avoid repeated operation
# Populate dictionary with candidate keys in indexed order.
for candidate in candidate_list:
    candidate_votes_dict[candidate] = 0

valid_first_line(ln1, quantity_of_candidates) # change debug print later
check_votes_validity_and_add_to_dictionary(lines_from_second, quantity_of_candidates)
print(candidate_votes_dict)

# fix check for numbers > candidate_quantity
# 