import requests
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def get_bs(url):
    try:
        html = requests.get(url)
    except HTTPError as e:
        print(e)
        return None
    bs = BeautifulSoup(html.text, 'html.parser')
    return bs

bs = get_bs('https://www.reuters.com/site-search/?query=data')
print(bs.select('ul'))
