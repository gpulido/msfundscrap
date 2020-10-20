from bs4 import BeautifulSoup
from dataclasses import dataclass
  
@dataclass
class MSFund:
    name: str
    ISIN: str # check format
    stars: int = 1 # change to range from 1-5
    vl: float = 0.0
    category: str  = "TEST" #to be reviewed
    common_expenses: int = 0
    sostenibility: int = 1#change to range from 1-5
    

def parse_table(table):
    values = {}    
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        name = ''
        value = ''
        for column in columns:            
            if not 'line' in column.attrs['class']:
                continue
            if 'heading' in column.attrs['class']:
                name = column.get_text()
            elif 'text' in column.attrs['class']:
                value = column.get_text()
        if name != '' and value != '':
            values[name] = value
    return values

def parse_general(soup_page):
    title = soup_page.title.string.split('|')
    #find stars variable
    stars_span = soup_page.findAll("span", {"class": "rating_sprite"})   
    stars = int(stars_span[0].attrs['class'][1][-1])
    #search for quickstats
    quickstats = soup_page.findAll("div", {"id": "overviewQuickstatsBenchmarkDiv"})[0].find('table')
    values = parse_table(quickstats)

    fund = MSFund(title[0], title[1], stars)
    print(fund)



soup = BeautifulSoup(open("src/example.html"), "html.parser")
#print(soup.prettify)
parse_general(soup)
