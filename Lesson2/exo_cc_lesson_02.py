# coding : utf-8
import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint
import pandas as pd
%matplotlib inline


def getWebDOM(url):
    res = requests.get(url)
    return res.text


def get_pc_list(url):
    soup = BeautifulSoup(getWebDOM(url), 'html.parser')
    pc_url_list = [a['href'] for a in soup.select("div.prdtBloc > a")]
    return pc_url_list


def getCategoryFigures(soup):
    try:
        new_price = soup.find_all(class_="fpPrice")[0]['content']
    except Exception as e:
        raise

    try:
        old_price = soup.select("#addForm span.fpStriked")[0]
        old_price = old_price.get_text().replace(' ', '').replace(
            '€', '').replace('*', '').replace(',', '.')
    except Exception as e:
        old_price = new_price

    return old_price, new_price


def get_prices(url, brand):
    dict = {}
    soup = BeautifulSoup(getWebDOM(url), 'html.parser')
    try:
        old_price, new_price = getCategoryFigures(soup)
        dict['brand'] = brand
        dict['old_price'] = old_price
        dict['new_price'] = new_price
    except Exception as e:
        return None

    return dict


if __name__ == "__main__":
    dell_list = "https://www.cdiscount.com/search/10/dell+pc+portable.html#_his_"
    acer_list = "https://www.cdiscount.com/search/10/acer+pc+portable.html#_his_"

    # pprint(dell_url_list)
    dell_prices = [get_prices(url, "Dell") for url in get_pc_list(dell_list)]
    # asus_prices=[get_prices(url) for url in get_pc_list(asus_list)]
    acer_prices = [get_prices(url, "Acer") for url in get_pc_list(acer_list)]

    prices = dell_prices + acer_prices

    df_prices = pd.DataFrame(prices)

    df_prices['rebate'] = (1 - df_prices["new_price"].astype('float64') /
                           df_prices["old_price"].astype('float64')) * 100

    df_rebates = df_prices.groupby("brand").mean()
    df_rebates.plot(kind="bar", figsize=(12, 6))
