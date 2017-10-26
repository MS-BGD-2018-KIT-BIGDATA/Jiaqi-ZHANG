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

if __name__ == "__main__":
    start_time = time.time()
    request = requests.get(
        "https://www.open-medicaments.fr/api/v1/medicaments?limit=100&query=IBUPROFENE")
    result = request.json()

    # pprint(result)
    records = []

    for row in result:
        dict = {}
        info = requests.get(
            "https://www.open-medicaments.fr/api/v1/medicaments/" + row['codeCIS']).json()
        dict['date']=info['dateAMM']
        dict['prix'] = info['presentations'][0]['prix']
        dict['labo'] = info['titulaires']
        # dict['equitrait']=info['presentations'][0]["libelle"]

        conteneur = re.search("[0-9]+", info['denomination']).group(0)
        nb_comprimes = re.search(
            "[0-9]+", info['presentations'][0]['libelle']).group(0)

        try:
            unite = re.search("[a-zA-Z]{0,1}g", info['denomination']).group(0)
        except AttributeError:
            unite = ""

        equitrait = int(conteneur) * int(nb_comprimes)

        dict['equitrait'] = str(equitrait) + " " + unite

        pprint(dict)

    # re=requests.get("https://www.open-medicaments.fr/api/v1/medicaments/64565560")

    # soup=BeautifulSoup(re.text,"html.parser")
    # pprint(re.json())

    # https://www.open-medicaments.fr/api/v1/medicaments/64565560
