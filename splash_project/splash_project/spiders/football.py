import scrapy
from scrapy_splash import SplashRequest

class FootballSpider(scrapy.Spider):
    name = "football"
    allowed_domains = ["adamchoi.co.uk"]

    script = '''
        function main(splash, args)
            splash: on_request(
                function(request)
                    request: set_header('User-Agent',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36') 
                end)
            
            splash.private_mode_enabled = false
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            assert(splash:go(args.url))
            assert(splash:wait(4))
            
            all_matches = splash:select('label[analytics-event="All matches"]')
            if all_matches then
                all_matches:mouse_click()
                assert(splash:wait(2))
            end

            splash:set_viewport_full()
            return {
                html = splash:html(),
                png = splash:png()
            }
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://www.adamchoi.co.uk/overs/detailed',
            callback=self.parse,
            endpoint='execute',
            args={'lua_source': self.script},
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
        )

    def parse(self, response):
        rows = response.xpath('//tr')

        for row in rows:
            date = row.xpath('./td[1]/text()').get()
            home_team = row.xpath('./td[2]/text()').get()
            score = row.xpath('./td[3]/text()').get()
            away_team = row.xpath('./td[4]/text()').get()
            yield {
                'date':date,
                'home_team':home_team,
                'score':score,
                'away_team':away_team,
            }