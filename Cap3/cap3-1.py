from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = []
def get_links(url):
    global pages
    html = urlopen('http://en.wikipedia.org{}'.format(url))
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.h1.get_text())
        print(bs.find(id="mw-content-text").find_all('p')[0])
        print(bs.find(id='ca-edit').find('a').attrs['href'])
    except AttributeError:
        print("this page is missing something! continuing whatever")
    for link in bs.find('div', {'id':'bodyContent'}).find_all(
    'a', href=re.compile(r"^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs and link.attrs['href'] not in pages:
            pages.append(link.attrs['href'])

get_links('')
i = 0
while len(pages) < 100000:
    page = pages[i]
    print(page)
    get_links(page)
    print('-' * 20)
    i+=1
