import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import requests
import time
import random
from datetime import date, timedelta
from db_reader import get_column_from_company, get_company_symbol
from PyQt6.QtCore import QDate

# get user's API key
api_key = None

def load_api_key():
    global api_key

    if api_key:
        return

    try:
        with open("../data/api_key.txt", "r") as f:
            api_key = f.read()
    except FileNotFoundError:
        pass

def change_in_stock_chart(company, start_date, end_date, *, save_data=False):
    # load user's api key
    load_api_key()

    # get company symbol from name
    symbol = get_company_symbol(company)

    # convert start_date and end_date to datetime objects
    start_date = date(start_date.year(), start_date.month(), start_date.day())
    end_date = date(end_date.year(), end_date.month(), end_date.day())
    
    # build base_url and params that will be consistent between every api call
    base_url = "https://api.twelvedata.com/eod"
    params = {
        "apikey": api_key,
        "symbol": symbol,
    }
    
    # initialize empty list to store data
    data = []

    # initialize date to increment

    # loop over every day between start date and end date, appending relevant data to the data list
    current_date = start_date
    while current_date <= end_date:
        params["date"] = current_date
        response = requests.get(base_url, params).json()
        try:
            data.append({
                "close": response["close"],
                "date": response["datetime"]
            })
            print(f"{response['datetime']}: {response['close']}")
        except KeyError:
            pass
        # https://docs.python.org/3/library/datetime.html
        current_date += timedelta(days=1)
        time.sleep(8)

    # convert data to pandas DataFrame
    df = pd.DataFrame(data)

    # convert columns from strings to the proper data time
    df["date"] = pd.to_datetime(df["date"])
    df["close"] = df["close"].astype("float64")

    # resize plot
    fig, ax = plt.subplots(figsize=(12, 10))

    # creating a loop that makes the line red when the score is decreasing, green when increasing, and gray otherwise
    prev = df["close"].iloc[0]
    colors = []

    # populate list of colors
    for i in range(1, len(df["close"])):
        curr = df["close"].iloc[i]
        if curr >= prev:
            colors.append("green")
        else:
            colors.append("red")
        prev = curr

    # plot data
    for i in range(1, len(df["close"])):
        ax.plot(df["date"].iloc[i-1:i+1], df["close"].iloc[i-1:i+1], "-o", color=colors[i-1])

    # setting minor and major locators for x axis
    # https://matplotlib.org/stable/gallery/text_labels_and_annotations/date.html
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,7)))

    # use month locator if data set is over 90 days, else use day locator
    if (df["date"].max() - df["date"].min()).days < 90:
        ax.xaxis.set_minor_locator(mdates.DayLocator())
    else:
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
    
    # applying formatter to x axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))

    # rotate x axis labels
    for label in ax.get_xticklabels(which="major"):
        label.set(rotation=30, horizontalalignment="right")

    ax.set_title(f"{company} Stock Value From {start_date} to {end_date}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Stock Price ($)")
    ax.grid()
    
    # save chart
    plt.savefig(f"../output/change_in_stock_{symbol}_{start_date}_to_{end_date}.png")
    
    plt.show()

    # save the data if the user requests it
    if save_data:
        df.to_csv(f"../output/change_in_stock_{symbol}_{start_date}_to_{end_date}.csv", index=False)
    
    

def sector_comparison_chart(date, *, save_data=False):
    # loads the user's api_key
    load_api_key()

    # convert QDate to string
    date = f"{date.year()}-{date.month()}-{date.day()}"

    # build base url and params that are consistent between api calls
    base_url = "https://api.twelvedata.com/eod"
    params = {
        "apikey": api_key,
        "date": date
    }

    # initialize empty list for storing data
    data = []

    # loop over every company in SMP 500, make call to api for closing price on the given date, and add it to data list
    for symbol, company, sector in get_column_from_company():
        params["symbol"] = symbol
        response = requests.get(base_url, params).json()

        try:
            data.append({
                "price": response["close"],
                "sector": sector
            })
            print(f"{company}: {response['close']}")
        except KeyError:
            print(f"something went wrong, skipping {company}")
        time.sleep(8)

    # convert data to pandas dataframe
    df = pd.DataFrame(data)

    # clean "N/A" and "n.a" sectors to be "Other"
    df["sector"] = df["sector"].map(lambda x: x if x not in ["N/A", "n.a"] else "Other")

    # change price column into float
    df["price"] = df["price"].astype("float64")

    # group all companies by their sectors and take the sum of their closing price
    grouped_df = df.groupby(by="sector").sum()

    # reset the sector back to being column
    grouped_df.reset_index(inplace=True)
    total_shares = grouped_df["price"].sum()

    # rename the sectors that make up less than 1.5% of all shares into "Other" for readability
    grouped_df.loc[grouped_df["price"] <= total_shares * 0.015, "sector"] = "Other"

    # regroup the sectors
    grouped_df = grouped_df.groupby(by="sector").sum()

    fig = plt.figure(figsize=(12, 10))
    # https://stackoverflow.com/questions/21572870/percent-label-position-in-pie-chart
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pie.html
    plt.pie(grouped_df["price"], labels=grouped_df.index, explode=[0.1 for _ in grouped_df["price"]], autopct='%1.1f%%', pctdistance=0.8, textprops=dict(rotation_mode = 'anchor', va='center', ha='center'))
    
    # https://saturncloud.io/blog/legend-outside-the-plot-in-python-matplotlib/
    plt.subplots_adjust(right=0.7)
    plt.legend(bbox_to_anchor=(1.5, 0), loc="lower right")
    
    # save chart
    plt.savefig(f"../output/sector_comparison_{date}.png")

    # display chart
    plt.show()

    # save the chart if the user wants to
    if save_data:
        df.to_csv(f"../output/sector_comparison_{date}.csv", index=False)


def currency_exchange_chart(currency, all_currencies, date, *, save_data=False):
    # loads the user's api key
    load_api_key()

    # convert QDate to string
    date = f"{date.year()}-{date.month()}-{date.day()}"
    
    # build base url and params that are consistent between all api calls
    base_url = "https://api.twelvedata.com/exchange_rate"
    params = {
        "apikey": api_key,
        "date": date
    }

    # initialize empty list to store data
    data = []

    # loop over all currency types, calling api to find the conversion between them and type of user's request. then add this data to the data list
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

    # convert data list to pandas dataframe
    df = pd.DataFrame(data, columns=["symbol", "rate"])

    # change the symbol of the chosen symbol to just be its symbol instead of being symbol/symbol
    df["symbol"] = df["symbol"].map(lambda x: x[4:] if len(x) > 3 else x)
    fig = plt.figure(figsize=(12, 10))

    # get random colors
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    colors = [random.choice(list(mcolors.TABLEAU_COLORS.keys())) for _ in range(len(df["symbol"]))]

    plt.bar(df["symbol"], df["rate"], color=colors)

    # https://www.geeksforgeeks.org/adding-value-labels-on-a-matplotlib-bar-chart/
    for i in range(len(df["symbol"])):
        plt.text(i, df["rate"].iloc[i], round(df["rate"].iloc[i], 2), ha="center")

    # rotate the ticks on the x axis by 90 degrees
    plt.xticks(rotation=90)

    # chart styling and axis labelling
    plt.title(f"{currency} Exchange Rates on {date} ")
    plt.xlabel("Currency Type")
    plt.ylabel(f"Exchange Rate per 1 {currency}")
    plt.title("% Makeup of SMP 500 by Sector")

    # save chart
    plt.savefig(f"../output/currency_exchange_{date}.png")

    plt.show()

    # save data
    if save_data:
        df.to_csv(f"../output/currency_exchange_{date}.csv", index=False)