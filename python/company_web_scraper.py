from splinter import Browser
from bs4 import BeautifulSoup

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import time

def get_company_names_and_symbols():
    # set up splinter
    browser = Browser("chrome")

    # visit a website with a list of all companies on sp500
    url = "https://www.slickcharts.com/sp500"
    browser.visit(url)

    # parse the website
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # initialize empty dictionary to store company names and symbols
    company_info = []

    # get the table
    table = soup.find("tbody")

    # iterate over every row in the table
    for row in table.find_all("tr"):
        # the company name and symbol are the only links in each row of the table, so get the text from them
        links = row.find_all("a")
        company_info.append([links[0].text, links[1].text])

    for company in company_info:
        browser.visit(f"https://www.sectorspdrs.com/stock/{company[1]}")
        time.sleep(5)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        try:
            # https://www.projectpro.io/recipes/pass-attributes-in-find-and-find-all-functions-of-beautiful-soup
            a = soup.find(lambda tag: tag.has_attr("aria-labelledby") and tag["aria-labelledby"] == "Sector")
            company.append(a.text)
            print(f"{company[1]}: {a.text}")
        except:
            print(f"{company[1]}: something messed up")
            company.append("N/A")
    print(company_info)

    # Creating database and filling with scraped company data
    # help from: https://stackoverflow.com/questions/16284537/creating-sqlite-database-if-it-doesnt-exist
    Base = declarative_base()

    class Company(Base):
        __tablename__ = 'companies'
        symbol = Column(String(255), primary_key=True)
        name = Column(String(255))
        sector = Column(String(255))

    engine = create_engine('sqlite:///../data/info.db')
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    # loop over every company in company_info and add it to database
    for company_name, symbol, sector in company_info:
        to_add = Company(symbol=symbol, name=company_name, sector=sector)
        session.add(to_add)

    # commit changes to database
    session.commit()

    # close the session
    session.close()

if __name__ == "__main__":
    get_company_names_and_symbols()