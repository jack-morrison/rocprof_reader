#!/usr/bin/env python3

''' --------------------------------------------------------------
 rocprof-reader.py
------------------------------------------------------------------

 `rocprof` generates output files in .csv format, which can be
 difficult to read. This program:

   * Reads in .csv files and prints the contents in columns
     for easier reading.

 There are also optional arguments to:

   * Remove long argument lists from kernel function names in the
     .stats.csv files

   * Change time format from ns to us, ms, or s

 NOTICE: This program currently only works with the default files
         that `rocprof` generates, with the following columns:

           * Name, Calls, TotalDurationNs, AverageNs, Percentage

-----------------------------------------------------------------
 Written by Tom Papatheodore
------------------------------------------------------------- '''

import argparse
import pandas as pd
import sys

# ===============================================================
# MAIN PROGRAM
# ===============================================================
def main():

    # Read in command line arguments 
    command_line_arguments = read_command_line_arguments()

    # Read in the data and re-format if needed
    data_frame = read_format(command_line_arguments)

    # Change time format if asked and print results
    format_print(data_frame, command_line_arguments)

 
# ===============================================================
# READ IN COMMAND LINE ARGUMENTS
# ===============================================================
def read_command_line_arguments():

    parser = argparse.ArgumentParser(description = 'This program prints rocprof .csv files in columns for easier reading.',
                                           usage = './%(prog)s --infile=<path-to-csv-file> [--no-args] [--time=<format>] [--help]')

    parser.add_argument('-n', '--no-args', action="store_true", help='remove argument list from kernel functions if too long.')
    parser.add_argument('-t', '--time'   , type=str, choices=["ns","us","ms","s"], default="ns", help='choose time format.')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--infile' , required=True, help='pass in the path to the rocprof .csv file you want to read.')

    args = parser.parse_args()

    return args


# ===============================================================
# READ IN THE DATA AND RE-FORMAT IF NEEDED/ASKED
# ===============================================================
def read_format(arguments):

    # Open rocprof file
    try:
        input_file_object = open(arguments.infile, "r")
    except IOError:
        print('There was an error opening the input file.')
        sys.exit(1)

    line_list = list()
    line_number = 0

    for line in input_file_object:

        # If the line has a function, it might have an argument list with commas
        if "(" in line:

            # Split line and add double quotes around function
            # since it has commas in the argument list.
            split_line=line.split("(")

            function_name  = split_line[0]
            argument_list  = split_line[1].split(")")[0]
            remaining_cols = split_line[1].split(")")[1]

            remaining_cols_list     = remaining_cols.split(",")
            remaining_cols_list[-1] = remaining_cols_list[-1].rstrip("\n")
            remaining_cols_list.pop(0)

            if arguments.no_args:
                line_list.append([function_name])
            else:
                # Put the line back together as a list to be passed to pandas dataframe
                line_list.append([function_name + "(" + argument_list + ")"])

            for element in remaining_cols_list:
                line_list[line_number].append(element)

        # Else, remove double quotes from headings (if found) and add to list to be 
        # passed to pandas dataframe
        else:

            split_line     = line.split(",")
            split_line[-1] = split_line[-1].rstrip("\n")
            list_length    = len(split_line)

            for i in range(0, list_length):
                split_line[i] = split_line[i].strip('"')

            line_list.append(split_line)    

        # Keep track of line number
        line_number = line_number + 1

    header_list = line_list[0]
    line_list.pop(0)

    df = pd.DataFrame(line_list, columns=header_list)

    return df


# ===============================================================
# CHANGE TIME FORMAT IF ASKED AND PRINT RESULTS
# ===============================================================
def format_print(df, arguments):

    df['Percentage']      = pd.to_numeric(df['Percentage'])
    df['TotalDurationNs'] = pd.to_numeric(df['TotalDurationNs'])
    df['AverageNs']       = pd.to_numeric(df['AverageNs'])
    
    if arguments.time == "ns":

        pass

    elif arguments.time == "us":

        df['TotalDurationNs'] = df['TotalDurationNs'].div(1000)
        df.rename(columns={'TotalDurationNs':'TotalDurationUs'}, inplace=True)

        df['AverageNs'] = df['AverageNs'].div(1000)
        df.rename(columns={'AverageNs':'AverageUs'}, inplace=True)

    elif arguments.time == "ms":

        df['TotalDurationNs'] = df['TotalDurationNs'].div(1000000)
        df.rename(columns={'TotalDurationNs':'TotalDurationMs'}, inplace=True)

        df['AverageNs'] = df['AverageNs'].div(1000000)
        df.rename(columns={'AverageNs':'AverageMs'}, inplace=True)

    elif arguments.time == "s":

        df['TotalDurationNs'] = df['TotalDurationNs'].div(1000000000)
        df.rename(columns={'TotalDurationNs':'TotalDurationS'}, inplace=True)

        df['AverageNs'] = df['AverageNs'].div(1000000000)
        df.rename(columns={'AverageNs':'AverageS'}, inplace=True)

    else:

        print("Something went wrong with the formatting.")

    print(df.to_string(index=False))


# ===============================================================
# IF RUN AS SCRIPT, EXECUTE MAIN
# ===============================================================
if __name__ == "__main__":
    main()
