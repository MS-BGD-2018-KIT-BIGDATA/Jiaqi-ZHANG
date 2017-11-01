import requests
from multiprocessing import Pool
import numpy as np
from bs4 import BeautifulSoup
import re
from pprint import pprint
from functools import partial
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

if __name__ == "__main__":
    sns.set()

    pd.set_option('display.expand_frame_repr', False)
    start_time = time.time()
    df_density_spe = pd.read_excel("C:/Users/Mauva/Documents/Work/INFMDI721/Lesson5/Effectif_et_densite_par_region_en_2014.xls",
                                   sheetname="Spécialistes")

    df_honoraires_spe = pd.read_excel(
        "C:/Users/Mauva/Documents/Work/INFMDI721/Lesson5/Conventionnement_par_region_en_2014.xls",
        sheetname="Spécialistes")

    df = pd.merge(df_density_spe, df_honoraires_spe,
                  on=["REGION INSEE", "Spécialistes"])

    df = df.rename(
        columns={"Spécialistes": "SPECIALISTES"})

    df_region = df[~df["SPECIALISTES"].str.contains(
        "TOTAL") & ~df["REGION INSEE"].str.contains("TOTAL")].copy()

    df_region.rename(
        columns={"DENSITE /100 000 hab.": "DENSITE"}, inplace=True)

    # Etudions dans un premier temps la corrélation entre densité
    # et taux de dépassement
    df_region_grouped = df_region.groupby("REGION INSEE").sum()
    df_region_grouped['RATIO_DEPASSEMENT'] = (
        df_region_grouped.TOTAL - df_region_grouped.CONVENTIONNES) /\
        df_region_grouped.TOTAL
    df_region_grouped = df_region_grouped.sort_values(
        "DENSITE", ascending=True)

    plt.figure(figsize=(18, 6))
    plt.plot(df_region_grouped['DENSITE'],
             df_region_grouped['RATIO_DEPASSEMENT'])

    plt.show()
    # On constate une tendance globale au dépassement d'honoraire lorsque la
    # densité augmente, mais l'erreur est tout de même importante.
    # On remarque que le taux est particulièrement élevé en IdF, le salaire
    # devrait avoir une forte corrélation avec le taux de dépassement.

    # Nous allons maintenant nous intéresser à l'IdF et à la région PACA, toutes
    # deux avec une forte densité et observer le taux de dépassement suivant les
    # Les spécialités.
    plt.figure(figsize=(18, 6))
    width = 0.3
    df_idf_paca = df_region[df_region['REGION INSEE'].str.contains(
        "11") | df_region['REGION INSEE'].str.contains("93")].copy()

    df_idf_paca['RATIO_DEPASSEMENT'] = (
        df_idf_paca.TOTAL - df_idf_paca.CONVENTIONNES) /\
        df_idf_paca.TOTAL

    ind = np.arange(df_idf_paca.shape[0] / 2)
    plt.xticks(ind, df_idf_paca[df_idf_paca['REGION INSEE'].str.contains(
        "11")]["SPECIALISTES"], rotation='vertical')

    plt.bar(ind - width / 2, df_idf_paca[df_idf_paca['REGION INSEE'].str.contains(
        "11")]['RATIO_DEPASSEMENT'], width)

    plt.bar(ind + width / 2, df_idf_paca[df_idf_paca['REGION INSEE'].str.contains(
        "93")]['RATIO_DEPASSEMENT'], width, color="darkorange")

    plt.tight_layout()
    plt.show()

    # A part en chirurgie, les dépassements sont sensiblement plus fréquents en IdF à l'exception
    # de l'obstétrique, ce qui peut paraître étonnant au premier abord mais peut être exliqué par
    # la rareté de la statistique en PACA.
