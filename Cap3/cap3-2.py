from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now().timestamp())

def get_internal_links(bs: BeautifulSoup, include_url):
    include_url = '{}://{}'.format(urlparse(include_url).scheme, urlparse(include_url).netloc)
    internal_links = []
    for link in bs.find_all('a', href=re.compile(r'^(/|.*' + include_url + ')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_links:
                if link.attrs['href'].startswith('/'):
                    internal_links.append(include_url + link.attrs['href'])
                else:
                    internal_links.append(link.attrs['href'])
    return internal_links

def get_external_links(bs: BeautifulSoup, exclude_url):
    external_links = []
    for link in bs.find_all('a', href=re.compile(r'^(http|www)((?!' + exclude_url + ').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])
    return external_links

def get_random_external_link(starting_page):
    html = urlopen(starting_page)
    bs = BeautifulSoup(html, 'html.parser')
    external_links = get_external_links(bs, urlparse(starting_page).netloc)
    if len(external_links) == 0:
        print('No external links, looking around the site for one')
        domain = '{}://{}'.format(urlparse(starting_page).scheme, urlparse(starting_page).netloc)
        internal_links = get_internal_links(bs, domain)
        return get_random_external_link(internal_links[random.randint(0, len(internal_links)-1)])
    else:
        return external_links[random.randint(0, len(external_links)-1)]

def get_random_internal_link(starting_page):
    html = urlopen(starting_page)
    bs = BeautifulSoup(html, 'html.parser')
    internal_links = get_internal_links(bs, urlparse(starting_page).netloc)
    if len(internal_links) == 0:
        print('no more lol')
        domain = '{}://{}'.format(urlparse(starting_page).scheme, urlparse(starting_page).netloc)
        print('Stopped at: ', domain)
        return
    else:
        return internal_links[random.randint(0, len(internal_links) - 1)]

def follow_external_only(starting_site):
    external_link = get_random_external_link(starting_site)
    print('Random External link is: {}'.format(external_link))
    follow_external_only(external_link)

def follow_internal(starting_site):
    internal = get_random_internal_link(starting_site)
    print('Random Internal link is: {}'.format(internal))
    follow_internal(internal)


if __name__=='__main__':
    follow_internal('https://www.wikipedia.org/')
