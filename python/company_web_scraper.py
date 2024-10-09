from splinter import Browser
from bs4 import BeautifulSoup

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# set up splinter
browser = Browser("chrome")

# visit a website with a list of all companies on sp500
url = "https://www.slickcharts.com/sp500"
browser.visit(url)

# parse the website
html = browser.html
soup = BeautifulSoup(html, "html.parser")

# initialize empty dictionary to store company names and symbols
company_info = {}

# get the table
table = soup.find("tbody")

# iterate over every row in the table
for row in table.find_all("tr"):
    # the company name and symbol are the only links in each row of the table, so get the text from them
    links = row.find_all("a")
    company_info[links[0].text] = links[1].text

print(company_info)

# Creating database and filling with scraped company data
# help from: https://stackoverflow.com/questions/16284537/creating-sqlite-database-if-it-doesnt-exist
Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    symbol = Column(String(255), primary_key=True)
    name = Column(String(255))

engine = create_engine('sqlite:///../data/info.db')
Base.metadata.create_all(engine)
session = Session(bind=engine)

# loop over every company in company_info and add it to database
for company_name, symbol in company_info.items():
    to_add = Company(symbol=symbol, name=company_name)
    session.add(to_add)

# commit changes to database
session.commit()

# close the session
session.close()