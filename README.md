# casestatus

A simple command line tool to check the staus of a [USCIS](https://egov.uscis.gov/casestatus/landing.do) case.
Created to make the process of querying for a set of recipt numbers a bit less cumbersome.

## Run it

Use the docker image to run with ease :

```
docker run -it --rm casestatus:edge casestatus -r MSC2190329165 MSC2190329170
```
## Build it

To build the image: 

```
docker build -t casestatus:edge .
```


## Local Install

casestatus is written in python, and you need python3 to run it. To install, Clone the repo

```
git clone https://github.com/jeevanjoseph/casestatus.git && cd casestatus
```

install the dependencies

```
pip install -r requirements.txt
```
or 
```
pip3 install -r requirements.txt
```
Done.

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
