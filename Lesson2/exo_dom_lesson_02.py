# coding : utf-8

import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint


def getWebDOM(url, params):
    res = requests.post(url, params)
    return res.text


def getCategoryFigures(table, category_name, year):
    table_row = table.find("td", text=re.compile("= "+category_name+"$")) \
        .parent

    category_title = table_row.select("td")[0].get_text()
    moyenne_habitant = table_row.select("td")[2].get_text()
    moyenne_strate = table_row.select("td")[3].get_text()
    if year not in tableau:
        tableau[year] = {}
    tableau[year][category_name] = {}
    tableau[year][category_name]['Catégorie'] = category_title
    tableau[year][category_name]['En euros par habitant'] = \
        moyenne_habitant.replace("\xa0", "")
    tableau[year][category_name]['Moyenne de la strate'] = \
        moyenne_strate.replace("\xa0", "")


if __name__ == "__main__":
    tableau = {}
    url = "http://alize2.finances.gouv.fr/communes/eneuro/tableau.php"
    years = list(range(2009, 2016))
    categories = ['A', 'B', 'C', 'D']
    params = {'ICOM': '056', 'DEP': '075', 'TYPE': 'BPS',
              'PARAM': 0, 'comm': 0}
    for year in years:
        params['EXERCICE'] = year
        soup = BeautifulSoup(getWebDOM(url, params), 'html.parser')
        table = soup.select("table:nth-of-type(4)")[0]
        for category in categories:
            getCategoryFigures(table, category, year)

    pprint(tableau)
