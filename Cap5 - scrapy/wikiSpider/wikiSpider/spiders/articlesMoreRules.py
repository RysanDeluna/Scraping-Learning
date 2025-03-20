from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ArticleSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [
        Rule(LinkExtractor(allow='^(/wiki/)((?!:).)*$'),
             callback='parse_items',
             follow=True,
             cb_kwargs={'is_article': True}),
        Rule(LinkExtractor(allow='.*'),
             callback='parse_items',
             cb_kwargs={'is_article': False})]


    def parse_items(self, response, is_article):
        print(response.url)
        title = response.xpath('//h1[@id="firstHeading"]//text()').get()
        if is_article:
            url = response.url
            text = response.xpath('//div[@id="mw-content-text"]//text()').get()
            last_updated = response.css('li#footer-info-lastmod::text').get()
            last_updated = last_updated.replace('This page was last edited on ', '')
            print('Title is: {}'.format(title))
            print('text is: {}'.format(text))
            print(last_updated)
        else:
            print('This is not an article: {}'.format(title))