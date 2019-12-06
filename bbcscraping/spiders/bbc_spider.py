import scrapy


class BBCSpider(scrapy.Spider):
    name = "bbc"
    start_urls = [
            'https://www.bbc.com/portuguese/geral-50260437',            
    ]
        
         
    def parse(self, response):

        text = response.css("div.story-body")[0]
        
        yield {
            'title': text.css("h1.story-body__h1::text").get(),
            'subtitle': text.css("div.story-body__inner p.story-body__introduction::text").get(),
        }

        next_page = response.css('ul.units-list a::attr(href)').get()
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

