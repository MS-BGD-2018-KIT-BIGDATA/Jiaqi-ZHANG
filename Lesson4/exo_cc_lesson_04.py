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


def get_details(medicament):
    dict = {}
    info = requests.get(
        "https://www.open-medicaments.fr/api/v1/medicaments/" + medicament['codeCIS']).json()
    dict['dateAMM'] = info['dateAMM']
    dict['prix'] = info['presentations'][0]['prix']
    dict['labo'] = info['titulaires']
    # dict['equitrait']=info['presentations'][0]["libelle"]

    dosage = re.search("[0-9]+", info['compositions'][0]
                       ['substancesActives'][0]['dosageSubstance']).group(0)

    try:
        nb_comprimes = re.search(
            "\d+", info['presentations'][0]['libelle']).group(0)
    except AttributeError:
        nb_comprimes = 0

    try:
        unite = re.search("\s{0,1}[a-zA-Z]{0,1}g\s{0,1}",
                          info['denomination']).group(0).replace(" ", "")
    except AttributeError:
        unite = ""

    equitrait = int(dosage) * int(nb_comprimes)

    indications = info["indicationsTherapeutiques"]

    dict['dosage'] = dosage + " " + unite
    dict['nb_comprimes'] = nb_comprimes
    dict['equitrait'] = str(equitrait) + " " + unite
    dict['indications'] = indications
    return dict


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)
    start_time = time.time()
    request = requests.get(
        "https://www.open-medicaments.fr/api/v1/medicaments?limit=100&query=IBUPROFENE")
    result = request.json()

    df = pd.DataFrame([get_details(medicament) for medicament in result])

    print(df)
