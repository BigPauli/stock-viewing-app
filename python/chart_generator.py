import pandas as pd
import matplotlib.pyplot as plt
import PIL as pillow
import datetime
import requests
import time
from db_reader import get_column_from_company, get_company_symbol

# get user's API key
api_key = None


def load_api_key():
    try:
        with open("../data/api_key.txt", "r") as f:
            api_key = f.read()
    except FileNotFoundError:
        pass

def change_in_stock_chart(company, start_date, end_date, *, save_data=False):
    if not api_key:
        load_api_key()
    
    print(company, start_date, end_date)

def stock_comparison_chart(company, date, *, save_data=False):
    if not api_key:
        load_api_key()

    print(company, date)

def currency_exchange_chart(currency, all_currencies, date, *, save_data=False):
    if not api_key:
        load_api_key()
    
    base_url = "https://api.twelvedata.com/exchange_rate"
    params = {
        "apikey": api_key,
        "date": f"{date.year()}-{date.month()}-{date.day()}"
    }
    data = []
    for currency_type in all_currencies:
        if currency_type == currency:
            data.append([currency, 1])
            continue
        params["symbol"] = f"{currency}/{currency_type}"
        response = requests.get(base_url, params).json()
        try:
            data.append([response["symbol"], response["rate"]])
        except KeyError:
            pass
        print(response)
        time.sleep(8)

    df = pd.DataFrame(data, columns=["symbol", "rate"])
    plt.bar(df["symbol"], df["rate"])
    plt.show()

# collecting sample data for testing purposes
if __name__ == "__main__":
    currency_exchange_chart("USD", ["USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "CNY", "NZD", "INR", "SEK", "ZAR", "HKD"], datetime.date.today(), save_data=True)