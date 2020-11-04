from bs4 import BeautifulSoup
from model import MSFund
from utils import *
from scrapper_motor import *
from selenium.webdriver.common.by import By

import logging

logger = logging.getLogger()

def parse_general(soup_page, fund):
    """ Parse the general page from ms

    Args:
        soup_page (soup page): Soup variable with the general page loaded
        fund (MsFund): The fund to fill with data from the general page
    """
    if soup_page == None:
        return
    title = soup_page.title.string.split('|')[0]
    fund.name = sanitize_text(title)
    #TODO: look for the ISIN
    
    rating_span = soup_page.findAll("span", {"class": "rating_sprite"})   
    #stars
    stars = rating_span[0].attrs['class'][1]
    fund.stars =  number_from_class(stars)
    #rating
    if len(rating_span) > 1:
        rating = rating_span[1].attrs['class'][1]
        fund.rating = rating_from_class(rating)

    #search for keystats
    keystats = soup_page.findAll("div", {"id": "overviewQuickstatsDiv"})[0].find('table')
    keystats_values = parse_table(keystats, "heading", "text") 
    #TODO: parse keystats values into fund
    fund.ISIN = keystats['ISIN']

    quickstats = soup_page.findAll("div", {"id": "overviewQuickstatsBenchmarkDiv"})[0].find('table')
    values = parse_table(quickstats, "heading", "text")    
    #TODO: parse quickstats values into fund   
    #Sustainability
    sust_div = soup_page.findAll("div", {"class": "sal-sustainability__score"})
    sust = number_from_class(sust_div[1].attrs['class'][1])
    fund.sustainability  = sust
   
    
def parse_rating_risk(soup_page, fund):
    """ Parse the rating risk page from ms

    Args:
        soup_page (soup page): Soup variable with the rating risk page loaded
        fund (MsFund): The fund to fill with data from the rating risk page
    """
    if soup_page == None:
        return
    left_table = soup_page.findAll("div", {"id": "ratingRiskLeftDiv"})[0].find('table')
    left = parse_table(left_table, "label", "value")
    right_table = soup_page.findAll("div", {"id": "ratingRiskRightDiv"})[0].find('table')
    right = parse_table(right_table, "label", "value")
    fund.sharpe = read_float_with_comma(right['Ratio de Sharpe'])    


def get_page_from_url(url, id_fund, tab = None, wait_locator = None, save_to_file = False):
    """Obtains the page from the url.
    Uses selenium to solve the dynamic loading of the page and if a wait_locator is
    provided selenium will wait until such locator appears on the page.

    Args:
        url (str): A well formed url to download 
        id_fund (str): MS id fund to be used on the files. TODO: review this param to abstract
        tab (int, optional): The ms fund tab page to retrieve, if none main page is download. Defaults to None.
        wait_locator (selenium locator, optional): locator that has to appear before selenium ends. Defaults to None.
        save_to_file (bool, optional): If true the downloaded page is stored on the file system. Defaults to False.

    Returns:
        soup page: a beautifulsoup parsed web
    """
    url_to_retrieve = url
    tab_name = "general"
    if tab != None:
        url_to_retrieve += "&tab=" + str(tab)
        tab_name = str(tab)
    
    logger.info(url_to_retrieve)
    page = get_page_selenium(url_to_retrieve, wait_locator)
    #page = get_page_requests(url_to_retrieve)

    if page == None:
        return None

    soup = BeautifulSoup(page, "html.parser")
    if save_to_file:
        with open(f"test_pages/{id_fund}_{tab_name}.html", "w") as f:
            print(soup.prettify, file=f)
    return soup


def parse_fund(id_fund):
    """Parses a fund given an morningstar id

    Args:
        id_fund (str): The morning star fund id to be parsed 
    
    Returns:
        MSFund: a MSFund instance with all the data filled
    """        
    url = f'https://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id={id_fund}'
    fund = MSFund()
    fund.MSID = id_fund
    
    general_page = get_page_from_url(url, id_fund, wait_locator = (By.ID, 'overviewQuickstatsBenchmarkDiv'), save_to_file=True)
    if general_page != None:
        parse_general(general_page, fund)      
        parse_rating_risk(get_page_from_url(url, id_fund, 2,  wait_locator = (By.ID, 'ratingRiskRightDiv'), save_to_file=True), fund)
    
    return fund


if __name__ == '__main__':
    with open('test_pages/0P000019YS_general.html', 'r') as f:
        contents = f.read()
    
    soup = BeautifulSoup(contents, "html.parser")
    fund = MSFund()
    fund.MSID = '0P000019YS'
    parse_general(soup, fund)
    #parse_fund("F0GBR04BG3")

