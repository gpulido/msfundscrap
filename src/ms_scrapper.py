import argparse
from model import *
from funds_filter import *
from fund_scrapper import *
from datetime import date
import itertools


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

    
def list_ids(args):
    """Use the provided list of ids to retrieve funds

    Args:
        args (str): A list of ms id's separated by commas
    """
    funds = args.list.split(',')    
    get_funds(funds, args.output, args.savefiles)     

def file_ids(args):
    """Use the provided list of ids to retrieve funds

    Args:
        args (str): A list of ms id's separated by commas
    """
    lines = [i.strip().split(',') for i in args.fileids.readlines()]
    args.fileids.close()
    funds = set(itertools.chain.from_iterable(lines))
    if '' in funds:
        funds.remove('')
    get_funds(funds, args.output, args.savefiles)    

def filter(args):
    """Use the provided filter args from the command line to generate the list of funds to
    retrieve from ms

    Args:
        args (args): Command line args with filter information
    """
    #create a ms fund filter with the args parameters
    newFilter = MSFundFilter()
    if args.star:
        newFilter.starRating = Levels(args.star)
    if args.rating:
        newFilter.quantitativeRating = QuaRatings[args.rating.upper()]
    if args.sustainability:
        newFilter.sustainabilityRating = Levels(args.sustainability)
    
    num, funds = get_funds_list_api(newFilter, 1, args.max)
    funds_ids = [f['SecId'] for f in funds] 
    if args.saveidsfile:
         with open(args.saveidsfile, 'w', newline='') as ids_file:
             ids_file.write(','.join(funds_ids))


    get_funds(funds_ids, args.output, args.savefiles)    

if __name__ == '__main__':    
    
    parser = argparse.ArgumentParser(prog='ms-scrapper-cli')
    parser.set_defaults(func=lambda args: parser.print_help())
    #TODO: validate output as path
    parser.add_argument('--output', type=str, default=f'data_{date.today()}.csv', help="output file to serialize to serialize the funds info")
    parser.add_argument('--loglevel', default='DEBUG', choices=['INFO', 'DEBUG'],  required=False, help="Logging level.", type=str)
    parser.add_argument('--savefiles', type=bool, default=False,  help="True if the html files should be stored")
    ids_parser = parser.add_subparsers(help="Specify how to obtain the ids")
    
    parser_list = ids_parser.add_parser("list", help="Specify list of ids")
    parser_list.add_argument("list", type=str, help="list of comma separated list of ms id's to grab info from")
    parser_list.set_defaults(func=list_ids)

    parser_list = ids_parser.add_parser("file", help="file with a comma separated list of ids")
    parser_list.add_argument("fileids", type=argparse.FileType('r'), help="file with a comma separated list")
    parser_list.set_defaults(func=file_ids)

    parser_filter = ids_parser.add_parser('filter', help="Filter to use to obtain the funds")
    parser_filter.add_argument("--star", type=int, choices=range(1, 6), help="min stars fund")
    parser_filter.add_argument("--rating", type=str, choices=["negative", "neutral", "bronze","silver", "gold"], help="min qualitative rating")
    parser_filter.add_argument("--sustainability", type=int, choices=range(1, 6), help="min sustainability rating")    
    parser_filter.add_argument("--saveidsfile", type=str, default = None, help="file where store the ids created by the filter")
    parser_filter.add_argument("--max", type=int, default=10,  help="maximun funds to scrap from the filter output")
    parser_filter.set_defaults(func=filter)

    args = parser.parse_args()
    #Configure logging
    logger = configure_logger(args.loglevel.upper())
    args.func(args)       
