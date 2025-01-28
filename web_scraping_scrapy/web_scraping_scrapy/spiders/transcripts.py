import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]
    # start_urls = ["https://subslikescript.com/movies"]
    start_urls = ["https://subslikescript.com/movies_letter-X"]

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url="https://subslikescript.com/movies_letter-X", headers={'user_agent': self.user_agent})

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,  # Sets a download delay of 0.5 seconds
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="scripts-list"]/li/a'), callback="parse_item", follow=True, process_request="set_user_agent"),
        Rule(LinkExtractor(restrict_xpaths='(//a[@rel="next"])[1]'), process_request="set_user_agent"),
        )

    def set_user_agent(self, request, spider): 
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        article = response.xpath('//article[@class="main-article"]')
        
        yield { 
            'title': article.xpath('./h1/text()').get(), 
            'plot': article.xpath('./p[@class="plot"]/text()').get(), 
            # 'transcript': article.xpath('./div[@class="full-script"]/div/p/text()').getall(),
            # 'transcript': article.xpath('./div[@class="full-script"]/div/p/text()').get(),
            'url': response.url, 
            # 'user-agent': response.request.headers['User-Agent'], 
        }
