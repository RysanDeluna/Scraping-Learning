from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from twisted.python.rebuild import lastRebuild


class ArticleSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [Rule(LinkExtractor(allow=r'.*'), callback='parse_items', follow=True)]

    def parse_items(self, response):
        url = response.url
        title = response.css('h1::text').extract_first()
        #text = response.xpath('//div[@id="mw-content-text"]//text()').extract()
        last_updated = response.css('li#footer-info-lastmod::text').extract_first()
        last_updated = last_updated.replace('This page was lasted edited on ', '')
        print('URL is: {}'.format(url))
        print('title is: {}'.format(title))
        #print('text is: {}'.format(text))
        print('last updated is: {}'.format(last_updated))