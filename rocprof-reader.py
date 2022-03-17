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

   * Print only the columns you want to view by providing a 
     comma-separated list of column names

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
                                           usage = './%(prog)s --infile=<path-to-csv-file> [--no-args] [--time=<format>] [--column-list=<comma-separated-list>] [--help]')

    parser.add_argument('-n', '--no-args'     , action="store_true", help='remove argument list from kernel functions if too long.')
    parser.add_argument('-t', '--time'        , type=str, choices=["ns","us","ms","s"], default="ns", help='choose time format.')
    parser.add_argument('-c', '--column-list' , type=str, help='provide a comma-separated list of column names you want to view.')

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

    with input_file_object:

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
# CHANGE TIME FORMAT IF ASKED AND PRINT COLUMNS (OR SUBSET)
# ===============================================================
def format_print(df, arguments):

    data_set_column_list = list(df.columns.values)

    # If the user specified columns to print, capture them in 
    # a list and make sure they are actually in the data set.
    if arguments.column_list is not None:

        column_names      = arguments.column_list
        column_names_list = column_names.split(',')
        column_names_list = [cname.strip() for cname in column_names_list]

        unknown_column_names = list(set(column_names_list) - set(data_set_column_list))

        if unknown_column_names:

            print(f'\nError! \n\nThe following column names given by the user were not found in the data set:')
            print(f'  {unknown_column_names}\n')
            print(f'The data set contains the following columns: ')
            print(f'  {data_set_column_list}\n')
            sys.exit(1)

    else:
        column_names_list = data_set_column_list

    # If the user specified a time format, convert the durations 
    # and update the column names as needed
    if arguments.time is not (None or "ns"):

        if arguments.time == "us":
            divide_by   = 1000.0
            time_prefix = "Us"
        elif arguments.time == "ms":
            divide_by   = 1000000.0
            time_prefix = "Ms"
        elif arguments.time == "s":
            divide_by   = 1000000000.0
            time_prefix = "S"
        else:
            error_message = "Something went wrong with the time formatting"
            sys.exit(error_message)

        column_number = 0
        for c in column_names_list:

            if "Ns" in c:
                df[c] = pd.to_numeric(df[c]).div(divide_by)
                column_names_list[column_number] = ''.join((c[:-2],time_prefix))
                df.rename(columns={c:column_names_list[column_number]}, inplace=True)

            column_number += 1

    print(df.to_string(index=False, columns=column_names_list))


# ===============================================================
# IF RUN AS SCRIPT, EXECUTE MAIN
# ===============================================================
if __name__ == "__main__":
    main()
