# Codetown Vote Display

## Introduction
This program, the Codetown vote Display, processes files containing election data to calculate and display results using the Borda Count method.\
\
It features a Graphical User Interface (GUI) built with Tkinter, allowing users to select input files (expected in .txt format by default) and view either the calculated election results or any error messages encoutered during processing.\
\
Input files are validated to ensure correct formatting before Borda Count calculation and sorting, and final result display.

## Features
* Loads, validates and display election data from appropriately formatted files.
* GUI for file selection and result/error display.
* Borda Count calculation for election results.
* Results displayed in descending point order, with a secondary alphabetical sort applied at tied point positions.
* Extensive input file validation. Checks:
    * Valid header line of candidate names.
    * Valid formatting and content of vote lines.
    * Each vote line contains a vote for all candidates.
    * Each vote line contains the same number of votes as overall candidates.
* Detailed error messages in GUI.
* Handles common file access errors.
* Resizable GUI window with a vertical scrollbar for viewing results or long messages.
* Horizontal wrapping of overly long lines.

## Installation
Prerequisites:
* Python 3.7+ (due to dictionary sorting behaviour).
* Tkinter (standard library with most Python installations).
* Vote files whose contents you wish to view/validate.
* No additional external dependencies.

<<<<<<< HEAD
Download the program files to your local machine and run main.py.
* In Windows, double click on main.py to run the program.
* In Linux, navigate to the directory in which you've placed it and, in
the terminal, run:\
    _python main.py_
=======
Download the program to your local machine and run vote_gui.py.
* In Windows, double click on vote_gui.py to run the program.
* In Linux, navigate to the directory in which you've placed it and, in
the terminal, run:\
    _python vote_gui.py_
>>>>>>> f5eb5a7c54f3724bde8c1bee287562b84c12b11f

## Usage
1. Run the program as described in the Installation section. The "Codetown Vote Display" GUI will appear.
2. Prepare your input file. A valid input file:
    * Has a first line consisting of candidate names separated by semicolons.
    * Each subsequent line has the rank assigned to each candidate by an individual voter, separated by a single semicolon for each ranking.
    * Each vote must provide a rank for all candidates listed in the header.
    * The number of rankings in each vote must match the number of candidates in the header.
    * Rankings should be in descending preference. ie. 1 = most preferred.
    * Example valid header and vote line:
        * Al Gorithm;Meg A. Byte;Chip Seton
        * 1;2;3
3. Click the **Find my file** button in the GUI. A file dialogue box will appear.
4. Navigate to your preferred file. The default filetype shown is txt, though you can also select to view all files.
5. Once you've selected your file, click the **Load file** buton.
6. The program will process the file:
    * If successful, the Borda Count results will be displayed in the GUI.
    * If any errors occur, a detailed error message will be displayed in the GUI.
        * If an error occured, you should try to load a new file.

<<<<<<< HEAD
## Program Structure
The program is organized into three modules:
* **main.py**: Entry point for the application.
* **vote_processor.py**: Contains the BordaVoteProcessor class with all vote processing logic.
* **gui.py**: Contains the VoteCounterGUI class with all interface components.

## Classes and Methods
### BordaVoteProcessor (vote_processor.py)
Handles all election data processing and validation.

#### load_file(filename)
=======
## Functions
### load_file(filename)
>>>>>>> f5eb5a7c54f3724bde8c1bee287562b84c12b11f
    Loads, validates and processes a vote data file.

    This function calls a series of child functions to achieve the following:
    1. Read the file referred by <handle_load_file_click>.
    2. Produce variables containing (1) the header line and (2) all subsequent 
        voteset lines.
    3. Validate the contents of the voting file.
    4. Produce a dictionary of counted and sorted results.

<<<<<<< HEAD
#### valid_first_line(ln1)
=======
### valid_first_line(ln1)
>>>>>>> f5eb5a7c54f3724bde8c1bee287562b84c12b11f
    Validates the first line (candidate names) of the file loaded.

    Checks:
    (1) The line is not empty.
    (2) There are no leading/trailing semicolons.
    (3) There are no multiple semicolons between candidate names.
    (4) There is at least one candidate.

<<<<<<< HEAD
#### check_votes_validity_and_export_to_list(ln1_candidates, lines_from_second)
=======
### check_votes_validity_and_export_to_list(ln1_candidates, lines_from_second)
>>>>>>> f5eb5a7c54f3724bde8c1bee287562b84c12b11f
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

<<<<<<< HEAD
#### calculate_and_sort_borda_results(ln1_candidates, meta_cleaned_votes_list)
=======
### calculate_and_sort_borda_results(ln1_candidates, meta_cleaned_votes_list)
>>>>>>> f5eb5a7c54f3724bde8c1bee287562b84c12b11f
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

<<<<<<< HEAD
### VoteCounterGUI (gui.py)
Manages the Tkinter interface and user interactions.

#### display_in_output_text(message_text)
=======
### display_in_output_text(message_text)
>>>>>>> f5eb5a7c54f3724bde8c1bee287562b84c12b11f
    Updates the content of the output Text widget.

    Runs through the following sequence when called:
    (1) Momentarily set the output textbox to normal (not read-only) to enable 
        editing.
    (2) Delete all text from the first line to the end.
    (3) Inserts the desired text.
    (4) Renders the widget read-only again.

<<<<<<< HEAD
#### open_file_dialog()
=======
### open_file_dialog()
>>>>>>> f5eb5a7c54f3724bde8c1bee287562b84c12b11f
    Opens a file dialogue for the user to select an input file.

    Updates the 'selected_file_path' StringVar and the 'label_file_selected'
        widget with the chosen file's path.
    Only the basename--filename and filetype stripped of directory--is 
        displayed. This is for brevity and user-friendliness.

<<<<<<< HEAD
#### handle_load_file_click()
=======
### handle_load_file_click()
>>>>>>> f5eb5a7c54f3724bde8c1bee287562b84c12b11f
    Handles the 'Load file' button click event.

    Retrieves the selected file's path, calls load_file(filename) to attempt to 
        load and process the file, and then displays either the Borda-counted 
        and sorted election results or an error message in the output text area.

    Passes filename to load_file(filename). <filename> is derived here from a 
        global variable rather than being received as an argument due to its 
        role in the GUI and maintainability concerns related to the likelihood 
<<<<<<< HEAD
        of ongoing tweaking of the GUI.
=======
        of ongoing tweaking of the GUI.
>>>>>>> f5eb5a7c54f3724bde8c1bee287562b84c12b11f
