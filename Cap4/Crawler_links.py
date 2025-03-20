import requests
from bs4 import BeautifulSoup

from WebSite_links import WebSite, Content
import re

class Crawler:
    def __init__(self, site: WebSite):
        self.site = site
        self.visited = []

    def get_page(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safe_get(self, page_obj, selector):
        selected_items = page_obj.select(selector)
        if selected_items is not None and len(selected_items) > 0:
            return '\n'.join([elem.get_text() for elem in selected_items])
        return ''

    def parse(self, url):
        bs = self.get_page(url)
        if bs is not None:
            title = self.safe_get(bs, self.site.title_tag)
            body = self.safe_get(bs, self.site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

    def crawl(self):
        bs = self.get_page(self.site.url)
        target_pages = bs.findAll('a', href=re.compile(self.site.target_pattern))
        for target_page in target_pages:
            target_page = target_page.attrs['href']
            if target_page not in self.visited:
                self.visited.append(target_page)
                if not self.site.absolute_url:
                    target_page = '{}{}'.format(self.site.url, target_page)
                self.parse(target_page)

if __name__ == '__main__':
    uol = WebSite('Uol', 'https://www.uol.com.br', '(/colunas/)', True, 'h1', 'p')
    crawler = Crawler(uol)
    crawler.crawl()
    print(len(crawler.visited))