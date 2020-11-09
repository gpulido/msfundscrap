# msfundscrap
Web scrapping of Funds information from MorningStart (https://www.morningstar.es/es/).

Tipología y ciclo de vida de los datos (Data Sciencie Master - UOC)

## members
- Alexis Germán Arroyo Peña
- Gabriel Pulido de Torres

## contents
The folder `pdf` contains the document **resolution of the practice** at [`pdf/documentoPractica1.pdf`](pdf/documentoPractica1.pdf)

The folder `src` contains Python source code for the scrapper.
- `src/ms_scrapper.py` - main entry point
- `src/fund_scraper.py` - Retrieves the information of a given fund
- `src/model.py` - Support classes to model funds and filters
- `src/ms_filter.py` -  Code that manage filters to the ms ids api.
- `src/utils.py` - Several helper functions
- `src/scrapper_motor.py` - Helper functions to retrieve pages using selenium or requests

(check the src [README](src/README.md) for detail instructions of usage.)



## dataset
DOI 10.5281/zenodo.4263256

URL https://doi.org/10.5281/zenodo.4263256
