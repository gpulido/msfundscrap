from model import *
import requests
from enum import Enum



ms_universes = { 
    MSUniverses.FUND:'FOESP$$ALL',
    MSUniverses.ETF:'ETEXG$XMAD|ETEUR$$ALL'
}

def get_ids_by_filter(fund_filter, page_number = 1, page_size = 100000):
    """Obtains the list of funds for the provided filter.
    As the ms api answer is paginated, two parameters are provided to retrieve them.
    However if the page_size is big enough the answer contains all data.

    Args:
        fund_filter ([type]): [description]
        page_number (int, optional): [description]. Defaults to 1.
        page_size (int, optional): [description]. Defaults to 100000.

    Returns:
        int, list[dict()]: Returns two values. The number of elements and a list of json elements
        that contains SecId and Isin data.
    """
    url = "https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security/screener"            
    params = {
              'page':page_number,
              'pageSize':page_size,
              'outputType':'json',              
              'version':1,
              'languageId':'es-ES',
              'currencyId':'EUR',
              'universeIds':ms_universes[fund_filter.universe],
              'securityDataPoints': 'SecId|Isin',              
    }
    if fund_filter != None:
        params['filters'] = fund_filter.to_api_filter()
                  
    r = requests.get(url, params=params).json()    
    num_funds = r['total']
    funds_list = r['rows']
    return num_funds, funds_list     


if __name__ == '__main__':
    test = MSFundFilter()
    test.starRating = Levels.FOUR
    test.sustainabilityRating = Levels.FOUR
    test.quantitativeRating = QuaRatings.SILVER
    print(test)
    get_ids_by_filter(test, 1, 10)


    