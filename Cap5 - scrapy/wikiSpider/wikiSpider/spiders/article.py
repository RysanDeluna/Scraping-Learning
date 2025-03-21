import scrapy

class ArticleSpider(scrapy.Spider):
    name = 'article'

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/Python_%28programming_language%29',
            'https://en.wikipedia.org/wiki/Monty_Python',
            'https://en.wikipedia.org/wiki/Functional_programming'
        ]
        return [scrapy.Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response):
        url = response.url
        title = response.xpath('//h1[@id="firstHeading"]//text()').get()
        print('URL is: {}'.format(url))
        print('Title is: {}'.format(title))
