# coding : utf-8

import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint


def getWebDOM(url):
    res = requests.get(url)
    return res.text


def getCategoryFigures(soup):
    old_price = soup.find_all(class_="fpStriked")[-1]
    new_price = soup.find_all(class_="fpPrice")[-1]

    return old_price.get_text().replace(' ','').replace('€','').replace('*','').replace(',','.'), new_price.get_text().replace(' ','').replace('€','.').replace('*','')

if __name__ == "__main__":
    model_dell_url = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/dell-dell-notebook-p0pmx-m5510-e3-1505m-16-g/f-1070992-del5397063944996.html"
    model_acer_url = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/acer-pc-portable-aspire-e5-774g-57p5-17-3-hd-ra/f-10709-aspiree5774g58j0.html?idOffre=154236317#mpos=6|cd"


    soup = BeautifulSoup(getWebDOM(model_dell_url), 'html.parser')
    old_price, new_price = getCategoryFigures(soup)
    rebate = (1 - float(new_price)/float(old_price)) * 100

    print("Dell:")
    print(old_price)
    print(new_price)
    print(rebate)

    soup = BeautifulSoup(getWebDOM(model_acer_url), 'html.parser')
    old_price, new_price = getCategoryFigures(soup)
    rebate = (1 - float(new_price)/float(old_price)) * 100

    print("Acer:")
    print(old_price)
    print(new_price)
    print(rebate)
