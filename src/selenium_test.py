id_fund = "F00000UDVS"
url = f"https://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id={id_fund}&tab=6"
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)# executable_path="/home/gpt/Desarrollo/UOC/msfundscrap/chromedriver")
driver.get(url)
with open(f"test_pages/{id_fund}_selenium.html", "w") as f:        
    print(driver.page_source, file=f)
driver.quit()