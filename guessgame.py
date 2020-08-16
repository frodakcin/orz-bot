from bs4 import BeautifulSoup
import random
import urllib
import urllib.request
import html5lib
import requests

KEY=""
SECRET=""

user = random.choice([
    "tmwilliamlin168",
    "frodakcin",
    "chezbgone",
    "pusheen",
    "Geothermal",
    "summitwei",
    "Jellyman102",
    "jainbot27",
    "thecodingwizard",
    "caoash",
    "BRCode",
    "nchn27"
])

r = requests.get(f'https://codeforces.com/api/user.status?handle={user}')

submissions = r.json()['result']
accepted_submissions = [(s['id'], s['contestId']) for s in submissions if s['verdict'] == 'OK']

x = random.choice(accepted_submissions)

def get_submission_code(x):
    """
    Input

        x: tuple(int, int) - (submission id, contest id)

    Output

        String: submission code

    """
    url = f'https://codeforces.com/contest/{x[1]}/submission/{x[0]}'

    r = requests.get(url)

    http_string = r.text

    soup = BeautifulSoup(http_string, 'html.parser')
    stuff = str(soup.find(id='program-source-text').string)
    return stuff
