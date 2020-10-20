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





generate_example("F00000UDVS")
