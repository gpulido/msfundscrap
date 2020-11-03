import requests
from bs4 import BeautifulSoup


def generate_example(id_fund):
    """
    Grab a single page and print as an html to inspect.
    This file can be loaded later onto beautifulsoup so it can be used for test without hitting the
    ms page.
    """
    general_page = requests.get(
        "https://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id=" + id_fund
    )
    soup = BeautifulSoup(general_page.content, "html.parser")
    with open(f"test_pages/{id_fund}_general.html", "w") as f:
        print(soup.prettify, file=f)

    sustainability_page = requests.get(
        f"https://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id={id_fund}&tab=6"
    )
    soup = BeautifulSoup(sustainability_page.content, "html.parser")
    with open(f"test_pages/{id_fund}_sustainability.html", "w") as f:
        print(soup.prettify, file=f)

    rating_risk_page = requests.get(
        f"https://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id={id_fund}&tab=2"
    )
    soup = BeautifulSoup(rating_risk_page.content, "html.parser")
    with open(f"test_pages/{id_fund}_rating_risk.html", "w") as f:
        print(soup.prettify, file=f)




###TEst code to move to funds_filter
def get_funds_resume(page_size, page_number):
    params = { 'page':1,
              'pageSize':100000,
              'outputType':'json',
              #'sortOrder':'LegalName',
              'version':1,
              'languageId':'es-ES',
              'currencyId':'EUR',
              'universeIds':'FOESP$$ALL',
              'securityDataPoints':'SecId|Isin'
              #'securityDataPoints':'SecId|SustainabilityRating|Isin'
              #'filterDataPoints':'BrandingCompanyId|IMASectorId|CategoryId|AdministratorCompanyId|UmbrellaCompanyId|GlobalAssetClassId|GlobalCategoryId|ShareClassType|BaseCurrencyId|AnalystRatingScale'
              #'filterDataPoints':'Id',              
    }
            #securityDataPoints=SecId%7CName%7CPriceCurrency%7CTenforeId%7CLegalName%7CClosePrice%7CYield_M12%7CCategoryName%7CAnalystRatingScale%7CStarRatingM255%7CQuantitativeRating%7CSustainabilityRank%7CReturnD1%7CReturnW1%7CReturnM1%7CReturnM3%7CReturnM6%7CReturnM0%7CReturnM12%7CReturnM36%7CReturnM60%7CReturnM120%7CFeeLevel%7CManagerTenure%7CMaxDeferredLoad%7CInitialPurchase%7CFundTNAV%7CEquityStyleBox%7CBondStyleBox%7CAverageMarketCapital%7CAverageCreditQualityCode%7CEffectiveDuration%7CMorningstarRiskM255%7CAlphaM36%7CBetaM36%7CR2M36%7CStandardDeviationM36%7CSharpeM36%7CTrackRecordExtension&filters=&term=&subUniverseId=     
    url = "https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security/screener"            
    r = requests.get(url, params=params)
    num_funds = r.json()['counts'][0]['total']
    
    #print(general_page)
    #url = "https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security/screener?languageId=es-ES&currencyId=EUR&universeIds=FOESP%24%24ALL&outputType=json&filterDataPoints=BrandingCompanyId%7CIMASectorId%7CCategoryId%7CAdministratorCompanyId%7CUmbrellaCompanyId%7CGlobalAssetClassId%7CGlobalCategoryId%7CShareClassType%7CBaseCurrencyId%7CAnalystRatingScale&filters="

# https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security/screener?page=1&pageSize=10&sortOrder=LegalName%20asc&outputType=json&version=1


get_funds_resume(1, 100000)