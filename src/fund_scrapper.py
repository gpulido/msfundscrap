from bs4 import BeautifulSoup
from model import MSFund, MSUniverses
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
    
    rating_span = soup_page.findAll("span", {"class": "rating_sprite"})
    if len(rating_span) > 0:
        #stars
        stars = rating_span[0].attrs['class'][1]
        fund.stars =  number_from_class(stars)
        #rating
        if len(rating_span) > 1:
            rating = rating_span[1].attrs['class'][1]
            fund.rating = rating_from_class(rating)
        #fund.rating = number_from_class(stars)

      
    quickstats = soup_page.findAll("div", {"id": "overviewQuickstatsBenchmarkDiv"})[0].find('table')
    values = parse_table(quickstats, "heading", "text")    
    fund.ISIN = values['ISIN']
    count = 1
    for key, k_value in values.items():
        
        if count == 1:
            key_plit = key.split("VL")
            fund.date_vl = key_plit[1]   
            fund.vl = k_value
        elif count == 2:
            fund.daily_change = sanitize_text(k_value)   
        elif count == 3:
            fund.category = k_value
        elif count == 5:
            key_plit = key.split("Patrimonio (Mil)")
            fund.date_heritage = key_plit[1]         
            fund.heritage = k_value 
        elif count == 6:
            key_plit = key.split("Patrimonio Clase (Mil)")
            fund.date_heritage_class = key_plit[1]   
            fund.heritage_class = k_value
        elif count == 7:
            fund.comission_max = sanitize_text(k_value)  
        elif count == 8:
            key_plit = key.split("Gastos Corrientes")
            fund.date_common_expenses = key_plit[1]   
            fund.common_expenses = k_value 
            
        count = count + 1
        
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

    volatilidad = left['Volatilidad']        
    if volatilidad == "-":  
        fund.volatility = 0.0
    else:
        v_split = volatilidad.split(" ")
        fund.volatility = read_float_with_comma(v_split[0])

    rentabilidad = left['Rentabilidad media 3a']
    if rentabilidad == "-":  
        fund.rentabilidad = 0.0
    else:
        r_split = rentabilidad.split(" ")
        fund.rentabilidad = read_float_with_comma(r_split[0])
    
    right_table = soup_page.findAll("div", {"id": "ratingRiskRightDiv"})[0].find('table')
    right = parse_table(right_table, "label", "value")  
    if right['Ratio de Sharpe'] != "-":
        fund.sharpe = read_float_with_comma(right['Ratio de Sharpe'])    
    else:
        fund.sharpe = 0.0


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


def parse_fund(id, universe = MSUniverses.FUND, save_to_file = False):
    """Parses a fund given an morningstar id

    Args:
        id_fund (str): The morning star fund id to be parsed 
    
    Returns:
        MSFund: a MSFund instance with all the data filled
    """    
    #logger.info(f'Scrapping {universe.name.lower()}: {id}')        
    logger.info(f'Scrapping : {id}')    
    #url = f'https://www.morningstar.es/es/{universe.name.lower()}s/snapshot/snapshot.aspx?id={id}'
    url = f'https://www.morningstar.es/es/{universe}s/snapshot/snapshot.aspx?id={id}'
    fund = MSFund()
    fund.MSID = id
    
    general_page = get_page_from_url(url, id, wait_locator = (By.ID, 'overviewQuickstatsBenchmarkDiv'), save_to_file=save_to_file)
    if general_page != None:
        parse_general(general_page, fund)      
        parse_rating_risk(get_page_from_url(url, id, 2,  wait_locator = (By.ID, 'ratingRiskRightDiv'), save_to_file=save_to_file), fund)
    
    return fund

def get_funds(list_id, universe, output, save_files):
    """Retrieve the current funds info for the provided list of ms ids and stores as csv into
    the provided output file path.
    Args:
        list_id (str): List of ms funds to retrieve info from.
        output (file path): A well formed file path
        save_files (boolean): True if the html files have to be download
    """    
    logger.info(f"Num of funds to retrieve: {len(list_id)}")
    logger.debug(list_id)
    logger.info("Scraping funds")
    
    #serialize to csv
    import csv
    with open(output, 'w', newline='') as csvfile:
        try:
            wr = csv.writer(csvfile, delimiter=',')
            dummy_fund = MSFund()
            wr.writerow(dummy_fund.get_properties_names())
            for id in list_id:
                fund = parse_fund(id, universe, save_files)
                wr.writerow(fund.get_properties())
        except Exception:
            logger.error("Error retrieving funds",  exc_info=True)


if __name__ == '__main__':
    with open('test_pages/F0GBR04I8O_general.html', 'r') as f:
        contents = f.read()
    
    soup = BeautifulSoup(contents, "html.parser")
    fund = MSFund()
    fund.MSID = 'F0GBR04I8O'
    parse_general(soup, fund)    

