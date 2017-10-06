# coding : utf-8
import requests
from multiprocessing import Pool
import numpy as np
from bs4 import BeautifulSoup
import re
from pprint import pprint
from functools import partial
import time
import pandas as pd


def getWebDOM(url):
    res = requests.get(url)
    return res.text


def getUserList(table):
    result = []
    rows = table.select("tr")
    result = [row.select("a:nth-of-type(1)")[0].get_text() for row in rows[1:257]]
    return result


def getUserStarMean(Token, user):
    repo_stars = 0
    git_api_url = "https://api.github.com"
    git_user_repos = requests.get(git_api_url + "/users/" + user + "/repos",
                                  auth=("archinul", Token))
    repo_list = [repo['stargazers_count'] for repo in git_user_repos.json()]
    repo_stars = np.mean(repo_list) if len(repo_list) > 0 else 0
    return user, repo_stars


if __name__ == "__main__":
    start_time = time.time()
    url = "https://gist.github.com/paulmillr/2657075"
    soup = BeautifulSoup(getWebDOM(url), 'html.parser')
    table = soup.select("table:nth-of-type(1)")[0]

    work_dir = "C:\\Users\\Mauva\\Documents\\Work\\INFMDI721\\Lesson3"

    with open(work_dir+'\\GitToken.txt') as fp:
        Token = fp.read().replace('\n', '')

    user_list = []
    user_list = getUserList(table)

    p = Pool()
    result = list(p.map(partial(getUserStarMean, Token), user_list))
    # [print(x[0] + ": " + str(np.round(x[1], 2))) for x in
    # #     sorted(result.items(), key=lambda x: (-1*x[1], x[0]))]
    df = pd.DataFrame.from_records(result, columns=['user', 'stars'])
    df_indexed = df.set_index("user")
    #
    print(df_indexed.sort_values(['stars'], ascending=False))

    print("--- %s seconds ---" % (time.time() - start_time))
