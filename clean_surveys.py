"""
The CDC's data set for the U.S. Chronic Disease Indicators include state-level
data for the most pressing indicators of public health. Some question include
results for multiple years. This program is to cull the questions for which 
more recent results are available.

Brent Jacobs 2017-07-07
"""
import os
import sys
from collections import defaultdict

def most_recent_years(fname, year_col, q_col, header = True):
    """
    Returns a dictionary mapping each question, as a string, to the most
    recent year it was asked, also as a string. 

    parameters:
        fname - string, name of a .csv file
        year_col - int, which column the years are in
        q_col - int, which column the question names are in
        header - bool, True if there is a header line
    """
    f = open(fname, "r")
    if header:
        f.readline
    
    yrs = defaultdict(int)

    for line in f.readlines():
        parts = line.split(",") 
        q = parts[q_col]
        y = parts[year_col]
        yrs[q] = max(yrs[q],y)

    f.close()

    return yrs

def clean_file(current_file_name, new_file_name, dict, col1, col2, header = True):
    """
    Copies the contents in current_file_name to new_file_name, removing any line where
    the value in column col2 does not map to the value in col1 in the dictionary dict

    parameters:
        current_file_name - string, name of the existing csv file
        new_file_name - string, name of the file to be written to
        dict - dictionary, mapping strings in col2 to strings in col1
        col1 - int, the number of a column (zero indexing)
        col2 - int, the number of a column (zero indexing)
        header - bool, if True the first line is copied over
    """
    old_file = open(current_file_name, "r")
    new_file = open(new_file_name, "w")

    if header:
        new_file.write(old_file.readline())

    for line in old_file.readlines():
        parts = line.split(",")
        if dict[parts[col2]] == parts[col1]:
            new_file.write(line) 

    old_file.close()
    new_file.close()

def append_year_to_different_column(curr_file_name, new_file_name, y_col, q_col, header = True):
    """
    Moves csv file in curr_file_name to a file called new_file_name, for each row appending
    it's year field to the end of another field
    
    parameters:
        curr_file_name - string, name of a csv file
        new_file_name - string, where the new file will be named
        y_col - int, which column contains the year (starting from 0)
        q_col - int, the column to which the year should be added
        header - bool, if there is a header line
    returns: None
    """

    old_file = open(curr_file_name, "r")
    new_file = open(new_file_name, "w")

    if header:
        new_file.write(old_file.readline())

    for line in old_file.readlines():
        parts = line.split(",")
        parts[q_col] += " (%s)" % parts[y_col] 
        new_line = ""
        for part in parts:
            new_line += part
            new_line += ","
        new_line = new_line[:-1]

        new_file.write(new_line)

    old_file.close()
    new_file.close()

def filter_csv(current_file_name, new_file_name, col, accepted, header = True, case_sensitive = True): 
    """ 
    Copies contents from csv file current_file_name to new_file_new, copying a 
    line if and only if the value in column number col is in the list accepted

    parameters:
        current_file_name - string, name of a csv file
        new_file_name - string, csv file to write to
        col - int, which column to filter on (starts at 0)
        accepted - list of strings, the accepted terms
        header - bool, True if the file has a header line
        case_sensitive - bool, True if the matching is to be case sensitive

    returns: None
    """
    old_file = open(current_file_name, "r")
    new_file = open(new_file_name, "w")

    if header:
        new_file.write(old_file.readline())

    if case_sensitive:
        for line in old_file.readlines():
            parts = line.split(",")
            if parts[col] in accepted:
                new_file.write(line)
    else:
        accepted = [s.lower() for s in accepted]
        for line in old_file.readlines():
            parts = line.split(",")
            if parts[col].lower in accepted:
                new_file.write(line)

    old_file.close()
    new_file.close()

def main():
    try:
        fname = sys.argv[1]
        newname = sys.argv[2]
    except IndexError:
        print "Please provide a filename for the current and for the new file."
        print "Use: python <remove_old_surveys.py> <existing_filename> <new_filename>"
        return 1

    temp_name1 = "temp.1csv" 
    temp_name2 = "temp2.csv"

    current_years = most_recent_years(fname, 1, 6)
    
    clean_file(fname, temp_name1, current_years, 1, 6) 

    append_year_to_different_column(temp_name1, temp_name2, 1, 6) 
    
    filter_csv(temp_name2, newname, 17, ["Overall"], case_sensitive = False) 

    os.remove(temp_name1)
    os.remove(temp_name2)
   

if __name__ == "__main__":
    main()
