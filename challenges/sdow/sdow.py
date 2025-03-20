import re
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import random
import datetime

def get_a_tags(bs: BeautifulSoup):
    return bs.find('div', {'id':'bodyContent'}).find_all(
        'a', href=re.compile(r"^(/wiki/)((?!:).)*$")
    )

def get_links(links):
    return [link['href'] if 'href' in link.attrs else None for link in links]


if __name__ == "__main__":
    random.seed(datetime.datetime.now().timestamp())
    URL = "https://en.wikipedia.org/wiki/Earth%27s_magnetic_field"
    bs = BeautifulSoup(urlopen(URL), 'html.parser')
    links = get_a_tags(bs)
    pages = get_links(links)
    it = 1
    searched = 'Stack_Overflow'
    pages_visited = []
    while len(pages) > 1:
        for page in pages:
            if '/wiki/{}'.format(searched) in page:
                print(f"FOUND!! after {len(pages_visited)} pages visited.")
                exit(0)
        next_page = pages.pop()
        while next_page in pages_visited:
            next_page = pages.pop()
        URL = 'https://en.wikipedia.org{}'.format(next_page)
        bs = BeautifulSoup(urlopen(URL), 'html.parser')
        pages_visited.append(next_page)
        pages.extend(get_links(get_a_tags(bs)))
        print(f"Visiting: {bs.h1.get_text()}")
