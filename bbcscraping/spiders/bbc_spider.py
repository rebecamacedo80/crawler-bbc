import scrapy

class QuotesSpider(scrapy.Spider):
    name = "bbc"

    start_urls = [
        # BRASIL 'https://www.bbc.com/portuguese/topics/cz74k717pw5t'
        'https://www.bbc.com/portuguese/topics/c404v027pd4t' #TECNOLOGIA
    ]

    def parse(self, response):

        for article in response.css('article'):

            link = article.css("a::attr(href)").extract_first()

            yield response.follow(link, self.parse_article)
        
        next_page = response.css('div.lx-pagination__controls.lx-pagination__controls--right.qa-pagination-right \
            a::attr(href)').get()
            
        if next_page is not None:
          yield response.follow(next_page, self.parse)

        
    def parse_article(self, response):

        text = response.css("div.story-body")[0]

        hiperlink = text.css("div.story-body__inner p.story-body__introduction a.story-body__link::text").get()

        subtitle = text.css("div.story-body__inner p.story-body__introduction::text").getall()

        if hiperlink is not None:
            if len(subtitle) > 1:
                subtitle = subtitle[0] + hiperlink + subtitle[len(subtitle)-1]
            else:
                pass
            
        else:
            subtitle = text.css("div.story-body__inner p.story-body__introduction::text").get()

        yield{
            'title': text.css("h1.story-body__h1::text").get(),
            'subtitle': subtitle
        }
