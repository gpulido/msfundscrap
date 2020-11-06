from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import requests



def get_sel_options():
    """Creates a selenium options pre-configured

    Returns:
        Options: a pre-configured selenium options 
    """
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    return options


def get_page(url, locator = None):
    """Retrieves the html of the given url
    It decides if use selenium or request

    Args:
        url (str): a well formed url to retrieve
        locator (Selenium locator, optional): Locator to wait. Defaults to None.

    Returns:
        str: The html source for the url
    """
    if locator != None:
        return get_page_selenium(url, locator)
    else:
        return get_page_requests(url)

def get_page_selenium(url, locator = None):
    """Uses selenium to retrieve the html code of a given url

    Args:
        url (urlstring): a well formed url 
        locator (string, optional): If given selenium will 
        wait until the element appears on the page. Defaults to None.

    Returns:
        str: html source text for the provided url
    """    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=get_sel_options())
    driver.get(url)
        
    try:        
        if locator:        
            element = WebDriverWait(driver, 5, poll_frequency=0.2).until(
                EC.presence_of_element_located(locator)
            )
    except:
        return None
    finally:               
        html_source = driver.page_source           
        driver.quit()

    return html_source


def get_page_requests(url):
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
                */*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch, br",
                "Accept-Language": "en-US,en;q=0.8",
                "Cache-Control": "no-cache",
                "dnt": "1",
                "Pragma": "no-cache",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
                37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
                }
    base_url = "https://www.morningstar.es/"

    r = requests.get(url, headers=headers, allow_redirects=False)
    return r.content


if __name__ == '__main__':
    get_page_requests("dummy")