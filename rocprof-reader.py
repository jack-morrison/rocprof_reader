#!/usr/bin/env python3

#-----------------------------------------------------
# This script takes `rocprof` CSV files and prints the 
# contents in readable columns
#
# Written by Tom Papatheodore
# ----------------------------------------------------

import csv
import argparse

# ===============================================================
# MAIN PROGRAM
# ===============================================================
def main():

    # Read in command line arguments 
    input_file, column_width = read_command_line_arguments()
    
    # Read in CSV file
    read_format_print(input_file, column_width)


# ===============================================================
# READ IN COMMAND LINE ARGUMENTS
# ===============================================================
def read_command_line_arguments():

    parser = argparse.ArgumentParser(
                description='This program is meant to make rocprof CSV files readable',
                usage='./%(prog)s --infile=<path-to-csv-file> [--cwidth=<width-of-columns>] [--help]')

    required_args = parser.add_argument_group('Required arguments:')   
    required_args.add_argument('-i', '--infile', required=True, help='Pass the rocprof CSV file you want to make readable.')
 
    parser.add_argument('-c', '--cwidth', required=False, type=str, help='Set the width of columns (in number of characters)', default=25)
    
    args = parser.parse_args()

    return args.infile, int(args.cwidth)


# ===============================================================
# READ CSV, FORMAT OUPUT, AND PRINT
# ===============================================================
def read_format_print(in_file, col_width):

    # Read in CSV file
    with open(in_file, newline='') as csvfile:

        rows = csv.reader(csvfile, delimiter=' ', quotechar='|')

        # Loop through rows of CSV file
        for row in rows:

            # Break the single-string list into a list with individual elements (i.e., columns)
            row_list = row[0].split(",")

            # Loop through columns of each row
            for column in row_list:

                # Remove double quotes from individual elements
                column = column.strip('\"')

                # If an element has more characters than column_width, truncate to (column_width - 1)
                if len(column) > col_width:
                    column = column[:col_width]

                # Calculate spaces needed for tidy columns
                num_spaces = col_width - len(column)

                print(column, " "*num_spaces, end='')

            print()


# ===============================================================
# IF RUN AS SCRIPT, EXECUTE MAIN
# ===============================================================
if __name__ == "__main__":
    main()
