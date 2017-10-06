import googlemaps
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
from pandas.io.json import json_normalize
from multiprocessing import Pool
from functools import partial
import time


def getWebDOM(url):
    res = requests.get(url)
    return res.text


def getTownVector(villes, Key, ville , distance_matrix=None):
    gmaps = googlemaps.Client(key=Key)
    if distance_matrix is None:
        distance_matrix = []
    distance_json = gmaps.distance_matrix(ville, villes)
    distance_normalized = json_normalize(
        distance_json, ['rows', 'elements'])['distance']
   #  distance_matrix[i].append([row['text'] for row in distance_normalized])
    distance_matrix += tuple([ville] + [row['text']
                                        for row in distance_normalized])
    # print(Key)
    # print(ville)
    return distance_matrix


if __name__ == "__main__":
    start_time = time.time()

    url = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es"
    soup = BeautifulSoup(getWebDOM(url), 'html.parser')
    table = soup.select("table:nth-of-type(1)")[0]
    rows = table.select("tr")
    work_dir = "C:\\Users\\Mauva\\Documents\\Work\\INFMDI721\\Lesson3"

    with open(work_dir+'\\Token.txt') as fp:
        Key = fp.read().replace('\n', '')

    villes = [row.select("a")[0].get_text() for row in rows[1:11]]

    p = Pool()
    distance_matrix = list(p.map(partial(getTownVector, villes, Key), villes))

    df = pd.DataFrame.from_records(
        distance_matrix, columns=["Villes"] + villes)
    df.to_csv(work_dir+"\\top_10_town_distance_matrix.csv", index=False, sep=";")

    print("--- %s seconds ---" % (time.time() - start_time))
