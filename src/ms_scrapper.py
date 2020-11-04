import argparse
from model import *
from funds_filter import *
from fund_scrapper import *


def configure_logger(logger_level):
    """Configure the python logger to show messages

    Args:
        logger_level (str): Level of logging to be used (DEBUG, INFO)

    Returns:
        logger: the configured logger
    """
    import logging
    numeric_level = getattr(logging, logger_level, None)
    logging.basicConfig(format= '%(asctime)s %(levelname)s:%(message)s', level=numeric_level)
    return logging.getLogger()


def get_funds(list_id, output):
    """Retrieve the current funds info for the provided list of ms ids and stores as csv into
    the provided output file path.
    NOTE: if there is a file with the 

    Args:
        list_id ([str]): List of ms funds to retrieve info from.
        output (file path): A well formed file path
    """    
    logger.info("Scraping funds")
    
    funds = [ parse_fund(id) for id in list_id]

    #serialize to csv
    import csv
    with open(output, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        dummy_fund = MSFund()
        wr.writerow(dummy_fund.get_properties_names())
        for fund in funds:
            wr.writerow(fund.get_properties())
    

def filter(args):
    """Use the provided filter args from the command line to generate the list of funds to
    retrieve from ms

    Args:
        args (args): Command line args with filter information
    """
    if args.input:
        logger.info("Found list of ids as input, ignore filter args")
        return

    #create a ms fund filter with the args parameters
    newFilter = MSFundFilter()
    if args.star:
        newFilter.starRating = Levels(args.star)
    if args.rating:
        newFilter.quantitativeRating = QuaRatings[args.rating.upper()]
    if args.sustainability:
        newFilter.sustainabilityRating = Levels(args.sustainability)
    
    num, funds = get_funds_list_api(newFilter,1, args.max)
    funds_ids = [f['SecId'] for f in funds]
    logger.info(f"Num of funds to retrieve: {num}")
    logger.debug(funds_ids)
    get_funds(funds_ids, args.output)    

if __name__ == '__main__':    
    
    parser = argparse.ArgumentParser(prog='ms-scrapper-cli')
    #TODO: validate output as path
    parser.add_argument("output", type=str, help="output file to serialize to serialize the funds info")
    parser.add_argument("--input", type=str, help="list of comma separated list of ms id's to grab info from")
    parser.add_argument('--loglevel', default='DEBUG', choices=['INFO', 'DEBUG'],  required=False, help="Logging level.", type=str)
    subparsers = parser.add_subparsers(help='filter help')
    parser_filter = subparsers.add_parser('filter', help="Filter to use to obtain the funds")
    parser_filter.add_argument("--star", type=int, choices=range(1, 6), help="min stars fund")
    parser_filter.add_argument("--rating", type=str, choices=["negative", "neutral", "bronze","silver", "gold"], help="min qualitative rating")
    parser_filter.add_argument("--sustainability", type=int, choices=range(1, 6), help="min sustainability rating")
    parser_filter.add_argument("--filterOutput", type=str, help="file where store the ids created by the filter")
    parser_filter.add_argument("--max", type=int, default=10,  help="maximun funds to scrap from the filter output")
    parser_filter.set_defaults(func=filter)

    args = parser.parse_args()
    #Configure logging
    logger = configure_logger(args.loglevel.upper())
    args.func(args)
   
    if args.input:
        get_funds(args.input, args.output)


