This folder contains the python code to use the scrapper.

## contents

- `ms_scrapper.py` - main entry point
- `fund_scraper.py` - Retrieves the information of a given fund
- `model.py` - Support classes to model funds and filters
- `ms_filter.py` -  Code that manage filters to the ms ids api.
- `utils.py` - Several helper functions
- `scrapper_motor.py` - Helper functions to retrieve pages using selenium or requests


## Usage
A command line utility is provided in ms_scrapper.py

```python
python ms_scrapper.py -h
```

```
usage: ms-scrapper-cli [-h] [--output OUTPUT] [--universe {fund,etf}] [--savefiles SAVEFILES] [--loglevel {INFO,DEBUG}] {list,file,filter} ...

positional arguments:
  {list,file,filter}    Specify how to obtain the ids
    list                Specify list of ids
    file                file with a comma separated list of ids
    filter              Filter to use to obtain the funds

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT       output file to serialize to serialize the funds info
  --universe {fund,etf}
                        type of ms universe to retrieve
  --savefiles SAVEFILES
                        True if the html files should be stored
  --loglevel {INFO,DEBUG}
                        Logging level.
```

### Use list of MS Ids as input

If a list of comma separated ids is provided the scapper will just get the info for then and save to the provided file

```
python ms_scrapper.py list FUND_ID1,FUND_ID2,FUND_ID3
```

### Use file with ids as input
If a file with ids is provided it will be parsed and use as input
example
```
python ms_scrapper.py file file_ids.txt
```
The expected format is a list of comma separated ids for each line.
Duplicates are removed


### Use filter as input

example:

```
python ms_scrapper.py filter --rating silver --star 4 --qualitative 3
```

A list of ids can be automatically obtained from ms using the filtering capabilities.
The filter categories currently supported are:

- MS Rating - use the `--rating` parameter (acepted values are "negative", "neutral", "bronze","silver", "gold")
- MS Stars - use the `--star` parameter (from 1 to 5)
- Qualitative - use the `--qualitative` parameter (from 1 to 5)

The parameters acts as a minimun value that should have, hence a --star 3 will retrieve funds with 3, 4 and 5 stars.
Several parameters can be combined, they behave as an `AND`

There is an extra parameter `--max` that limits the number of funds retrieved
