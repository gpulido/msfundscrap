from bs4 import BeautifulSoup
from dataclasses import dataclass
import locale

def read_float_with_comma(num):
    return float(num.replace(",", "."))
    #return locale.atof(num)
    
  
@dataclass
class MSFund:
    """Class to keep information of funds.
    The use of a class allows to better abstraction and allows to 
    define several output formats
    """

    ISIN: str # check format
    name: str = None
    stars: int = 1 # change to range from 1-5
    vl: float = 0.0
    category: str  = None #to be reviewed
    common_expenses: int = 0
    Sustainability: int = 1#change to range from 1-5
    sharpe: float = 0.0
    

def parse_table(table, header_class, value_class):
    """Parses a TR / TD table from MS 
    TODO: move to the helpers

    Args:
        table (soup table): Soup table loaded from MS

    Returns:
        [dictionary]: dictionary with the values of the table
    """
    values = {}    
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        name = ''
        value = ''
        for column in columns:            
            # if not 'line' in column.attrs['class']:
            #     continue
            if header_class in column.attrs['class']:
                name = column.get_text()
            elif value_class in column.attrs['class']:
                value = column.get_text()
        if name != '' and value != '':
            values[name] = value
    return values

def parse_general(soup_page, fund):
    """ Parse the general page from ms

    Args:
        soup_page (soup page): Soup variable with the general page loaded
        fund (MsFund): The fund to fill with data from the general page
    """

    title = soup_page.title.string.split('|')
    fund.name = title
    #find stars variable
    stars_span = soup_page.findAll("span", {"class": "rating_sprite"})   
    stars = int(stars_span[0].attrs['class'][1][-1])
    fund.stars = stars
    #search for quickstats
    quickstats = soup_page.findAll("div", {"id": "overviewQuickstatsBenchmarkDiv"})[0].find('table')
    values = parse_table(quickstats, "heading", "text")    
    #TODO: parse quickstats values into fund    
    #Sustainability
    sust_div = soup_page.findAll("div", {"class": "sal_sustainability__score"})
    sust = int(sust_div[0].attrs['class'][1][-1])
    fund.Sustainability  = sust   
    

def parse_rating_risk(soup_page, fund):
    """ Parse the general page from ms

    Args:
        soup_page (soup page): Soup variable with the rating risk page loaded
        fund (MsFund): The fund to fill with data from the rating risk page
    """
    left_table = soup_page.findAll("div", {"id": "ratingRiskLeftDiv"})[0].find('table')
    left = parse_table(left_table, "label", "value")
    right_table = soup_page.findAll("div", {"id": "ratingRiskRightDiv"})[0].find('table')
    right = parse_table(right_table, "label", "value")
    fund.sharpe = read_float_with_comma(right['Ratio de Sharpe'])    




#TODO: Test code to be removed when the proper calls are implemented
isin = 'F00000UDVS'
general = BeautifulSoup(open(f'test_pages/{isin}_general.html'), "html.parser")
rating_riks = BeautifulSoup(open(f'test_pages/{isin}_rating_risk.html'), "html.parser")
fund = MSFund(isin)
#print(soup.prettify)
parse_general(general, fund)
parse_rating_risk(rating_riks, fund)
print(fund)
