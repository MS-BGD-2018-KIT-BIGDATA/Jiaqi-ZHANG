import requests
from multiprocessing import Pool
import numpy as np
from bs4 import BeautifulSoup
import re
from pprint import pprint
from functools import partial
import time
import pandas as pd
import sys


def get_car_list(region, version, vendeur, car_list_url):
    url = ("https://www.leboncoin.fr/voitures/offres/"
           "{region}/?q={version}&brd=Renault&mdl=Zoe&f={vendeur}")
    res = requests.get(url.format(region=region,
                                  version=version,
                                  vendeur=vendeur))

    car_list_page = BeautifulSoup(res.text, "html.parser")
    car_list_href = car_list_page.select("li[itemscope] > a:nth-of-type(1)")
    [car_list_url.append(['https:' + x['href'], version, vendeur])
     for x in car_list_href]
    return car_list_url


def get_car_specs(url, version, vendeur):
    car_dict = {}
    res = requests.get(url)
    car_page = BeautifulSoup(res.text, "html.parser")

    price = car_page.select("span.value")[0].get_text()
    release_date = car_page.select("span.value")[4].get_text()
    kilometrage = car_page.select("span.value")[5].get_text()
    description = car_page.select("p[itemprop='description']")[0].get_text()

    try:
        price = re.search("[0-9]+", price.replace(' ', '')).group(0)
    except AttributeError:
        price = ""

    try:
        release_date = re.search("[0-9]{4}", release_date).group(0)
    except AttributeError:
        release_date = ""

    try:
        kilometrage = re.search(
            "[0-9]+", kilometrage.replace(' ', '')).group(0)
    except AttributeError:
        kilometrage = ""

    desc_parsed = description.replace(' ', '').replace('.', '')

    try:
        tel_fixe = re.search(
            "((\+|00)33\s?|0)[1](\s?\d{2}){4}", desc_parsed).group(0)
    except AttributeError:
        tel_fixe = ""

    try:
        tel_port = re.search(
            "((\+|00)33\s?|0)[67](\s?\d{2}){4}", desc_parsed).group(0)
    except AttributeError:
        tel_port = ""

    type_vendeur = {"p": "particulier", "c": "professionnel"}

    car_dict['version'] = modele
    car_dict['price'] = int(price)
    car_dict['kilometrage'] = kilometrage
    car_dict['release_date'] = release_date
    car_dict['tel_fixe'] = tel_fixe
    car_dict['tel_port'] = tel_port
    car_dict['type_vendeur'] = type_vendeur[vendeur]

    return car_dict


def get_cote_argus(version, year, kilometrage):
    url = ("https://www.lacentrale.fr/"
           "cote-auto-renault-zoe-{version}-{year}.html")
    res = session.get(url.format(version=version,
                                 year=year), headers=headers)

    url_cote_perso = "https://www.lacentrale.fr/get_co_prox.php?km={km}"
    res = session.get(url_cote_perso.format(km=kilometrage), headers=headers)

    return int(res.json()['cote_perso'])


if __name__ == "__main__":
    start_time = time.time()
    work_dir = "C:\\Users\\Mauva\\Documents\\Work\\INFMDI721\\Lesson4"
    headers = {
        'User-Agent': ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)"
                       " AppleWebKit/537.36 (KHTML, like Gecko)"
                       " Chrome/39.0.2171.95 Safari/537.36")}

    regions = ["ile_de_france", "aquitaine", "provence_alpes_cote_d_azur"]
    # regions = ["ile_de_france"]
    modeles = ["life", "zen", "intens"]
    # modeles = ["life"]
    vendeurs = ["p", "c"]
    # vendeurs = ["p"]
    car_list_url = []
    [get_car_list(r, m, v, car_list_url)
     for r in regions for m in modeles for v in vendeurs]

    car_specs = []
    car_specs += [get_car_specs(x[0], x[1], x[2]) for x in car_list_url]
    df = pd.DataFrame(car_specs)

    # print(df[['version','release_date','kilometrage']])
    argus_list = []
    session = requests.Session()
    argus_list = [get_cote_argus(
        row.version, row.release_date, row.kilometrage)
        for row in df.itertuples()]

    df_argus = pd.DataFrame(argus_list, columns=["cote argus"])
    df = pd.concat([df, df_argus], axis=1, join_axes=[df.index])

    df['comparaison argus'] = '='
    df.loc[df['price'] > df['cote argus'], 'comparaison argus'] = '+'
    df.loc[df['price'] < df['cote argus'], 'comparaison argus'] = '-'

    df.to_csv(work_dir + "\\leboncoin_zoe_offer.csv",
              index=False, sep=";")

    print("--- %s seconds ---" % (time.time() - start_time))
    # pprint(df)
