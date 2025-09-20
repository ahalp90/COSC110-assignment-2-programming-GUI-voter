"""
Backend vote processing logic for Codetown Vote Display.

This module handles all election data processing using the Borda Count method.
"""

class BordaVoteProcessor:
    """Processes election data files and calculates results using Borda Count method."""
    
    def load_file(self, filename):
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
            ln1_candidates = self.valid_first_line(ln1)

            # Validate vote lines and convert them to a single list of 
            # voteset integer lists.
            meta_cleaned_votes_list = self.check_votes_validity_and_export_to_list(
                ln1_candidates, lines_from_second)
            
            # Borda-calculate and sort a dictionary from the results.
            sorted_borda_dict = self.calculate_and_sort_borda_results(
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

    def valid_first_line(self, ln1):
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

    def check_votes_validity_and_export_to_list(self, ln1_candidates, lines_from_second):
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

    def calculate_and_sort_borda_results(self, ln1_candidates, meta_cleaned_votes_list):
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