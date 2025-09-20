"""
Codetown Vote Display

This program processes files containing election data to calculate and display 
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

from gui import VoteCounterGUI


def main():
    """Main entry point for the Codetown Vote Counter application."""
    app = VoteCounterGUI()
    app.run()


if __name__ == "__main__":
    main()