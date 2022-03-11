# :thumbsup: `rocprof_reader`

This program is meant to take `rocprof` CSV output files as input and print out the content in easy-to-read columns.

```python
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

------------------------------------------------------------- '''
```

```
$ ./rocprof-reader.py --help
usage: ./rocprof-reader.py --infile=<path-to-csv-file> [--no-args] [--time=<format>] [--help]

This program prints rocprof .csv files in columns for easier reading.

optional arguments:
  -h, --help            show this help message and exit
  -n, --no-args         remove argument list from kernel functions if too long.
  -t {ns,us,ms,s}, --time {ns,us,ms,s}
                        choose time format.

required arguments:
  -i INFILE, --infile INFILE
                        pass in the path to the rocprof .csv file you want to read.
```


### Contributing
If you have potential contributions, please feel free to open an issue.
