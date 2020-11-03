from urllib.request import urlretrieve
from urllib.parse import urlencode
from .model import *
from .selenium_scrapper import *


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
    page = get_page_selenium(url,  "ec-screener-results-view-container-group-section-panel-all")

    with open(f"test_pages/search_fund_selenium2.html", "w") as f:        
        print(page, file=f)





test = MSFundFilter()
test.starRating = 5
url = generate_search_url(fund_filter)
get_fund_list(url)

    