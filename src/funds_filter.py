from urllib.request import urlretrieve
from urllib.parse import urlencode
from model import *
from scrapper_motor import *
import requests


def generate_search_url(filtersSelectedValue):
    """[summary]

    Args:
        filtersSelectedValue ([type]): [description]

    Returns:
        [type]: [description]
    """
    baseUrl = "https://www.morningstar.es/es/screener/fund.aspx"
    params = {'filtersSelectedValue': filtersSelectedValue.to_filter_json(), 
        'page': 1,
        'sortField':'legalName',
        'sortOrder': 'asc'}   
        
    return f'{baseUrl}#?{urlencode(params)}'


def get_fund_list(url):
    page = get_page_selenium(url, (By.ID, "ec-screener-results-view-container-group-section-panel-all"))



def get_funds_list_api(fund_filter, page_number = 1, page_size = 100000):
    """Obtains the list of funds for the provided filter.
    As the ms api answer is paginated two parameters are provided to retrieve them.
    However if the page_size is big enough the answer contains all data.

    Args:
        fund_filter ([type]): [description]
        page_number (int, optional): [description]. Defaults to 1.
        page_size (int, optional): [description]. Defaults to 100000.

    Returns:
        int, list[dict()]: Returns two values. The number of elements and a list of json elements
        that contains SecId and Isin data.
    """
    params = {
              'page':page_number,
              'pageSize':page_size,
              'outputType':'json',              
              'version':1,
              'languageId':'es-ES',
              'currencyId':'EUR',
              'universeIds':'FOESP$$ALL',
              'securityDataPoints':'SecId|Isin',
              #'securityDataPoints':'SecId|SustainabilityRating|Isin'
              #'filterDataPoints':'BrandingCompanyId|IMASectorId|CategoryId|AdministratorCompanyId|UmbrellaCompanyId|GlobalAssetClassId|GlobalCategoryId|ShareClassType|BaseCurrencyId|AnalystRatingScale'
              #'filterDataPoints':'Id',  
              #'filters':'starRatingM255:IN:4:5'
    }
    if fund_filter != None:
        params['filters'] = fund_filter.to_api_filter()
            #securityDataPoints=SecId%7CName%7CPriceCurrency%7CTenforeId%7CLegalName%7CClosePrice%7CYield_M12%7CCategoryName%7CAnalystRatingScale%7CStarRatingM255%7CQuantitativeRating%7CSustainabilityRank%7CReturnD1%7CReturnW1%7CReturnM1%7CReturnM3%7CReturnM6%7CReturnM0%7CReturnM12%7CReturnM36%7CReturnM60%7CReturnM120%7CFeeLevel%7CManagerTenure%7CMaxDeferredLoad%7CInitialPurchase%7CFundTNAV%7CEquityStyleBox%7CBondStyleBox%7CAverageMarketCapital%7CAverageCreditQualityCode%7CEffectiveDuration%7CMorningstarRiskM255%7CAlphaM36%7CBetaM36%7CR2M36%7CStandardDeviationM36%7CSharpeM36%7CTrackRecordExtension&filters=&term=&subUniverseId=     
    url = "https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security/screener"            
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
    get_funds_resume(test, 1, 100000)


    