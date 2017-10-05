# coding : utf-8
import requests
from multiprocessing import Pool
import numpy as np
from bs4 import BeautifulSoup
import re
from pprint import pprint
import time


def getWebDOM(url):
    res = requests.get(url)
    return res.text


def getUserList(table):
    result = []
    rows = table.select("tr")
    for row in rows[1:257]:
        result.append(row.select("a:nth-of-type(1)")[0].get_text())
    return result


def getUserStarMean(user):
    repo_stars = 0
    TOKEN = "cd2e34b1b0a71e3c3ba581ec5be37c3ae0a48176"
    git_api_url = "https://api.github.com"
    git_user_repos = requests.get(git_api_url + "/users/" + user + "/repos",
                                  auth=("archinul", TOKEN))
    repo_list = [repo['stargazers_count'] for repo in git_user_repos.json()]
    repo_stars = np.mean(repo_list) if len(repo_list) > 0 else 0
    return user, repo_stars


if __name__ == "__main__":
    start_time = time.time()
    url = "https://gist.github.com/paulmillr/2657075"
    soup = BeautifulSoup(getWebDOM(url), 'html.parser')
    table = soup.select("table:nth-of-type(1)")[0]

    user_list = []
    user_list = getUserList(table)

    p = Pool()
    result = dict(p.map(getUserStarMean, user_list))

    [print(x[0] + ": " + str(np.round(x[1], 2))) for x in
        sorted(result.items(), key=lambda x: (-1*x[1], x[0]))]

    print("--- %s seconds ---" % (time.time() - start_time))
