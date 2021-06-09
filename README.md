# casestatus

A simple command line tool to check the staus of a [USCIS](https://egov.uscis.gov/casestatus/landing.do) case.
Created to make the process of querying for a set of recipt numbers a bit less cumbersome.

## Usage

```
casestatus.py [-h] [-r receipt_num_start receipt_num_end] [receipt_numbers ...]

Check status of USCIS cases.

positional arguments:
  receipt_numbers       enter the receipt numbers to check for

optional arguments:
  -h, --help            show this help message and exit
  -r receipt_num_start receipt_num_end, --range receipt_num_start receipt_num_end
                        enter the receipt number range
``` 
