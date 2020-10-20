from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

id_fund = "F0GBR04BG3"
url = f"https://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id={id_fund}"

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(url)
with open(f"test_pages/{id_fund}_selenium.html", "w") as f:        
    print(driver.page_source, file=f)
driver.quit()