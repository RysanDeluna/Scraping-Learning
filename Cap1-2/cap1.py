from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def get_bs(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    bs = BeautifulSoup(html.read(), 'html.parser')
    return bs

title = get_bs('http://www.pythonscraping.com/pages/page1.html').h1
if title is None:
    print("Title could not be found")
else:
    print(title)
