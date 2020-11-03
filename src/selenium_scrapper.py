from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

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