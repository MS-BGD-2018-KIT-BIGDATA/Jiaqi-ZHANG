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
%matplotlib inline

if __name__ == "__main__":
    start_time = time.time()
    df_density = pd.read_csv(
        "C:/Users/Mauva/Documents/Work/INFMDI721/Lesson5/rpps-medecins-tab10.csv",
        sep=";",
        encoding='latin-1')

    del df_density['Ensemble des spécialités']
    del df_density['Spécialistes']
    df_density_long = pd.melt(
        df_density, id_vars=['REGION ACTIVITE'], var_name='Specialite')

    df_grouped = df_density_long.groupby(['REGION ACTIVITE']).sum()
    # print(df_grouped.head())
    df_grouped.sort_values('value', ascending=False).plot(kind="bar", figsize=(12, 6))

    # print(df_grouped)
    # df_gouped.plot(df_grouped['REGION ACTIVITE'], df_grouped['value'])
    # print("--- %s seconds ---" % (time.time() - start_time))

    # pprint(df)
