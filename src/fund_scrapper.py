from bs4 import BeautifulSoup
from model import MSFund, MSUniverses, quarating_from_class
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
        #rating
        rating = rating_span[0].attrs['class'][1]
        fund.rating =  number_from_class(rating)
        #Quantitative rating
        if len(rating_span) > 1:
            quarating = rating_span[1].attrs['class'][1]
            fund.quarating = quarating_from_class(quarating)        

      
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
        
    
    
def parse_sustainability(soup_page, fund):
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

    fund.volatility = get_float_from_dict(left, 'Volatilidad', True)
    fund.rentabilidad = get_float_from_dict(left, 'Rentabilidad media 3a', True)  

    right_table = soup_page.findAll("div", {"id": "ratingRiskRightDiv"})[0].find('table')
    right = parse_table(right_table, "label", "value")

    fund.sharpe = get_float_from_dict(right, 'Ratio de Sharpe')
    


def get_page_from_url(id, universe, tab = None, wait_locator = None, save_to_file = False):
    """Obtains the page .
    Uses selenium to solve the dynamic loading of the page and if a wait_locator is
    provided selenium will wait until such locator appears on the page.

    Args:       
        id(str): MS id fund to be used on the files. TODO: review this param to abstract
        tab (int|str, optional): The ms fund tab page to retrieve, if none main page is download. Defaults to None.
        wait_locator (selenium locator, optional): locator that has to appear before selenium ends. Defaults to None.
        save_to_file (bool, optional): If true the downloaded page is stored on the file system. Defaults to False.

    Returns:
        soup page: a beautifulsoup parsed web
    """
    url = f'https://www.morningstar.es/es/{universe}s/snapshot/' 
    
    if tab == None:      
        url_to_retrieve = f'{url}snapshot.aspx?id={id}'
        tab_name = "general"
    elif tab == 'p':
        url_to_retrieve = f'{url}p_snapshot.aspx?id={id}'
        tab_name = str(tab)    
    else:
        url_to_retrieve = f'{url}snapshot.aspx?id={id}&tab={str(tab)}'
        tab_name = str(tab)
        
    logger.info(url_to_retrieve)
    page = get_page(url_to_retrieve, wait_locator)
    
    if page == None:
        return None

    soup = BeautifulSoup(page, "html.parser")

    if save_to_file:
        with open(f"test_pages/{id}_{tab_name}.html", "w") as f:
            print(soup.prettify, file=f)
    return soup


def parse_fund(id, universe = MSUniverses.FUND, save_to_file = False):
    """Parses a fund given an morningstar id

    Args:
        id (str): The morning star fund id to be parsed
        universe (MSUniverses): The type of universe to retrieve
        save_to_file: If true the htmls are saved to the local storage also
    
    Returns:
        MSFund: a MSFund instance with all the data filled
    """        
    logger.info(f'Scrapping : {id}')            
    fund = MSFund()
    fund.MSID = id
    
    print_page = get_page_from_url(id, universe, tab='p', save_to_file=save_to_file)        
    if print_page != None:
        parse_general(print_page, fund)              
        parse_rating_risk(print_page, fund)
        #sustainability is not in print page    
        sustainability_page = get_page_from_url(id, universe.name.lower(), tab=6, wait_locator = (By.CLASS_NAME, 'sal-sustainability__score'), save_to_file=save_to_file)    
        parse_sustainability(sustainability_page, fund)    
    
    return fund

def get_funds(list_id, universe, output, save_files):
    """Retrieve the current funds info for the provided list of ms ids and stores as csv into
    the provided output file path.
    Args:
        list_id (str): List of ms funds to retrieve info from.
        output (file path): A well formed file path
        save_files (boolean): True if the html files have to be download
    """    
    num_funds = len(list_id)
    logger.info(f"Num of funds to retrieve: num_funds")
    logger.debug(list_id)
    logger.info("Scraping funds")
    
    #serialize to csv
    import csv
    count = 0
    with open(output, 'w', newline='') as csvfile:
        try:
            wr = csv.writer(csvfile, delimiter=',')
            dummy_fund = MSFund()
            wr.writerow(dummy_fund.get_properties_names())
            for id in list_id:
                count += 1
                logger.info(f"Scrapin fund {count}/{num_funds}")
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

