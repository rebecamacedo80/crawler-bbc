import scrapy

class BBCSpider(scrapy.Spider):
    name = "bbc"

    start_urls = [
        # 'https://www.bbc.com/portuguese/topics/cz74k717pw5t' # BRASIL 
        # 'https://www.bbc.com/portuguese/topics/cvjp2jr0k9rt' # ECONOMIA
        # 'https://www.bbc.com/portuguese/topics/c340q430z4vt' # SAÚDE
        'https://www.bbc.com/portuguese/topics/cr50y580rjxt' # CIÊNCIA
        # 'https://www.bbc.com/portuguese/topics/c404v027pd4t' # TECNOLOGIA

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

        title = text.css("h1.story-body__h1::text").get()

        subtitle = response.css('meta[name="description"]::attr(content)').get()

        yield{
            'title': title,
            'subtitle': subtitle
        }