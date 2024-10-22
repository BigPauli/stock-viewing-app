import random
import pandas as pd
from chart_generator import line_chart_from_df, pie_chart_from_df, bar_chart_from_df
from db_reader import get_column_from_company, get_company_symbol
from datetime import date, timedelta


def mock_change_in_stock_chart(company, start_date, end_date, *, save_data=False):
    # get company symbol from name
    symbol = get_company_symbol(company)

    # convert start_date and end_date to datetime objects
    start_date = date(start_date.year(), start_date.month(), start_date.day())
    end_date = date(end_date.year(), end_date.month(), end_date.day())

    # build random starting stock value between 0 and 200 USD
    value = random.uniform(0, 200)

    # initialize empty list to store data
    data = []

    # initialize date to increment
    current_date = start_date

    # loop over every day between start date and end date, appending relevant data to the data list
    while current_date <= end_date:
        data.append({
            "close": value,
            "date": current_date
        })

        # randomly change value by -10 to 10
        value += random.uniform(-10, 10)

        current_date += timedelta(days=1)

    # convert data to pandas DataFrame
    df = pd.DataFrame(data)

    # create line chart with data
    line_chart_from_df(df, symbol, company, start_date, end_date, save_data=save_data, mock=True)


def mock_sector_comparison_chart(date, *, save_data=False):
    # convert QDate to string
    date = f"{date.year()}-{date.month()}-{date.day()}"

    # initialize empty list for storing data
    data = []

    # loop over every company in S&P 500, generate a random number between 0 and 200, add it to data list
    for symbol, company, sector in get_column_from_company():
        data.append({
            "price": random.uniform(0, 200),
            "sector": sector
        })

    # convert data to pandas DataFrame
    df = pd.DataFrame(data)

    pie_chart_from_df(df, date, save_data=save_data, mock=True)


def mock_currency_exchange_chart(currency, all_currencies, date, *, save_data=False):
    # convert QDate to string
    date = f"{date.year()}-{date.month()}-{date.day()}"

    # initialize list to store data
    data = []

    # loop over all currency types, generating random number between 0 and 100
    for currency_type in all_currencies:
        if currency_type == currency:
            data.append([currency, 1])
        else:
            data.append([f"{currency}/{currency_type}", random.uniform(0, 100)])

    # convert data list to pandas DataFrame
    df = pd.DataFrame(data, columns=["symbol", "rate"])

    bar_chart_from_df(df, currency, date, save_data=save_data, mock=True)