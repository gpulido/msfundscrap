from bs4 import BeautifulSoup
from .model import MSFund
from .utils import *

def rating_from_class(rating_class):
    number = int(rating_class[-1])
    if number == 1:
        return "Negative"
    if number == 2:
        return "Neutral"
    if number == 3:
        return "Bronze"
    if number == 4:
        return "Silver"
    if number == 5:
        return "Gold"
    if number == 6:
        return "Under Review"
    if number == 7:
        return "Not Ratable"    
    return None

def parse_general(soup_page, fund):
    """ Parse the general page from ms

    Args:
        soup_page (soup page): Soup variable with the general page loaded
        fund (MsFund): The fund to fill with data from the general page
    """

    title = soup_page.title.string.split('|')[0]
    fund.name = sanitize_text(title)
    
    rating_span = soup_page.findAll("span", {"class": "rating_sprite"})   
    #stars
    stars = rating_span[0].attrs['class'][1]
    fund.stars =  number_from_class(stars)
    #rating
    if len(rating_span) > 1:
        rating = rating_span[1].attrs['class'][1]
        fund.rating = rating_from_class(rating)

    #search for quickstats
    quickstats = soup_page.findAll("div", {"id": "overviewQuickstatsBenchmarkDiv"})[0].find('table')
    values = parse_table(quickstats, "heading", "text")    
    #TODO: parse quickstats values into fund   
    #Sustainability
    sust_div = soup_page.findAll("div", {"class": "sal-sustainability__score"})
    sust = number_from_class(sust_div[1].attrs['class'][1])
    fund.Sustainability  = sust
   
    
def parse_rating_risk(soup_page, fund):
    """ Parse the rating risk page from ms

    Args:
        soup_page (soup page): Soup variable with the rating risk page loaded
        fund (MsFund): The fund to fill with data from the rating risk page
    """
    left_table = soup_page.findAll("div", {"id": "ratingRiskLeftDiv"})[0].find('table')
    left = parse_table(left_table, "label", "value")
    right_table = soup_page.findAll("div", {"id": "ratingRiskRightDiv"})[0].find('table')
    right = parse_table(right_table, "label", "value")
    fund.sharpe = read_float_with_comma(right['Ratio de Sharpe'])    


def get_page_from_url(url, tab = None):
    url_to_retrieve = url
    if tab != None:
        url_to_retrieve += "$tab=" + str(tab)
    
    page = requests.get(url_to_retrieve)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def parse_fund(id_fund):
    """Parses a fund given an morningstar id

    Args:
        id_fund (str): The morning star fund id to be parsed 
    
    Returns:
        MSFund: a MSFund instance with all the data filled
    """    
    #id_fund = "F0GBR04BG3"
    url = f"https://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id={id_fund}"
    fund = MSFund()
    fund.MSID = id_fund
    
    parse_general(get_page_from_url(url), fund)    
    parse_rating_risk(get_page_from_url(url, 2), fund)
    
    return fund

parse_fund("F0GBR04BG3")

