import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["qiushibaike.com"]
    start_urls = [
        'https://www.qiushibaike.com/hot/',
    ]
    tmp = 0;
    def parse(self, response):

        for quote in response.css('div.article'):
            yield {
                'text': quote.css('span::text').extract_first(),
                'author':quote.css("div.author h2::text").extract(),
                'likes':quote.css("i.number::text").extract_first(),
            }
        if(self.tmp==0):
            next_page = response.css("ul.pagination li a::attr(href)")[5].extract()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
            self.tmp=self.tmp+1