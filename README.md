# <img src="./thumbsup.png" width="40"> `rocprof_reader`

This program is meant to take `rocprof` CSV output as input and output the content in easy-to-read columns.

```
$ ./rocprof-reader.py --help
usage: ./rocprof-reader.py --infile=<path-to-csv-file> [--cwidth=<width-of-columns>] [--help]

This program is meant to make rocprof CSV files readable

optional arguments:
  -h, --help            show this help message and exit
  -c CWIDTH, --cwidth CWIDTH
                        Set the width of columns (in number of characters)

Required arguments::
  -i INFILE, --infile INFILE
                        Pass the rocprof CSV file you want to make readable.
```


### Contributing
If you have potential contributions, please feel free to open an issue.
