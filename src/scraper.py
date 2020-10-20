from bs4 import BeautifulSoup
from dataclasses import dataclass
#import locale


def sanitize_text(text):
    return text.replace('\n', '').strip()

def read_float_with_comma(num):
    return float(num.replace(",", "."))
    #return locale.atof(num)
    
def number_from_class(number_class):
    """Helper method to return the last char as integer from a numbered
    class. example: stars1 stars2 stars3

    Args:
        number_class (str): class name that has a number at the end

    Returns:
        int: the number representation of the class.
    """
    return int(number_class[-1])

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
    rating: str = None
    

def parse_table(table, header_class, value_class):    
    """Parses a TR / TD table from MS 
    TODO: move to the helpers

    Args:
        table (soup table): Soup table loaded from MS
        header_class(str): the name of the css class that identifies header columns
        value_class(str): the name of the css class that identifies value columns

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
general = BeautifulSoup(open(f'test_pages/{isin}_general2.html'), "html.parser")
rating_riks = BeautifulSoup(open(f'test_pages/{isin}_rating_risk.html'), "html.parser")
fund = MSFund(isin)
#print(soup.prettify)
parse_general(general, fund)
parse_rating_risk(rating_riks, fund)
print(fund)
