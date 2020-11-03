from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlretrieve
from urllib.parse import urlencode
from model import *

def get_sel_options():
    """Creates a selenium options pre-configured

    Returns:
        Options: a pre-configured selenium options 
    """
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    return options


def get_page_selenium(url, wait_for_element = None):
    """Uses selenium to retrieve the html code of a given url

    Args:
        url (urlstring): a well formed url 
        wait_for_element (string, optional): If given selenium will 
        wait until the element appears on the page. Defaults to None.

    Returns:
        str: html source text for the provided url
    """
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=get_sel_options())
    driver.get(url)
    #yield driver.page_source
    #TODO: review if we can use yield and reuse the driver passing a collection
    try:        
        if wait_for_element:        
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, wait_for_element))
            )
    finally:               
        html_source = driver.page_source                  
        driver.quit()

    return html_source

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

    