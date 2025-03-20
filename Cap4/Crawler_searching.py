import requests
from Website_searching import Content, WebSite
from bs4 import BeautifulSoup

class Crawler:
    def get_page(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safe_get(self, page_obj: BeautifulSoup, selector):
        """
        Used to get a content string based on a bs4 and selector
        :param page_obj:
        :param selector:
        :return:
        """
        child_obj = page_obj.select(selector)
        if child_obj is not None and len(child_obj) > 0:
            return child_obj[0].get_text()
        return ""


    def search(self, topic, site: WebSite):
        """
        Search in a given website a given topic and registers all found pages
        :param topic:
        :param site:
        :return:
        """
        bs = self.get_page(site.search_url + topic)
        search_result = bs.select(site.result_list)
        for result in search_result:
            url = result.select(site.result_url)[0].attrs["href"]
            bs = self.get_page(url) if site.absolute_url else self.get_page(site.url + url)
            if bs is None:
                print("Something was wrong with that page or URL. Skipping...")
                return
            title = self.safe_get(bs, site.title_tag)
            body = self.safe_get(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body, topic)
                content.print()


    def parse(self, site: WebSite, url):
        """
        Extract content from a given url
        :param site:
        :param url:
        :return:
        """

        bs = self.get_page(url)
        if bs is not None:
            title = self.safe_get(bs, site.get_title_tag())
            body  = self.safe_get(bs, site.get_body_tag())
            if title != "" and body != "":
                content = Content(url, title, body, "")
                content.print()


if __name__ == '__main__':
    crawler = Crawler()

    site_data = [
        # NAME - URL - TITLE_TAG - BODY_TAG - SEARCH_URL - RESULT_LIST - RESULT_URL - ABSOLUTE_URL
        ['Brookings', 'https://www.brookings.edu/', 'h1', 'div.post-body', 'https://www.brookings.edu/?s=', 'div.content ol.articles-stream', 'article.article a', True]
    ]
    websites=[]
    for row in site_data:
        websites.append(WebSite(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    topics = ['Data', 'Brazil']
    for topic in topics:
        print('GETTING INFORMATION ABOUT: '+ topic)
        for target in websites:
            crawler.search(topic.replace(' ','+'), target)