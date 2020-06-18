import scrapy
import pandas as pd
import re

class BBCSpider(scrapy.Spider):
    name = "bbc"
    def start_requests(self):        
        urls = []        
        df = pd.read_csv('/home/rebeca/LinksNotícias/linksExtraídosBBCBrasil/linksMergePREPROCESSED.csv', sep=';')

        for index, row in df.iterrows():
            link = row['links']
            urls.append('http://'+link)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        text = response.css("div.story-body")
        title = text.css("h1.story-body__h1::text").get()
        sub = text.css("div.story-body__inner p.story-body__introduction").get()
        subtitle = re.sub('<[^>]*>', '', str(sub)) # regex para eliminar tags, caso haja
       
        if sub == None: # se não encontra subtítulo pega primeiro parágrafo da notícia            
            if title == None: # se não encontra título provavelmente é uma notícia em vídeo
                text = response.css("div#root main")
                title = text.css("div.GridItemConstrainedLarge-sc-12lwanc-4.gVouae strong::text").get()
                sub = text.css("div.GridItemConstrainedMedium-sc-12lwanc-2.fVauYi p").get()
                subtitle = re.sub('<[^>]*>', '', str(sub))

                if title == None or sub == None: # se ainda não encontrar texto, ignora e segue
                    pass                
                else:
                    yield{
                        'title': title,
                        'subtitle': subtitle
                    }            
            else:
                sub = text.css("div.story-body__inner p").get()
                subtitle = re.sub('<[^>]*>', '', str(sub))

                if sub == None: # se ainda não encontrar texto, ignora e segue
                    pass
                else:
                    yield{
                        'title': title,
                        'subtitle': subtitle
                    }
        else:
            if sub == '.': # correção para páginas que não têm subtítulo explicito
                sub = text.css("div.story-body__inner p").get()
                subtitle = re.sub('<[^>]*>', '', str(sub))
                        
            yield{
                'title': title,
                'subtitle': subtitle
            }

        

# ---------------------------------------------------------------------------------------------------------------- #

""" start_urls = [
        # 'https://www.bbc.com/portuguese/topics/cz74k717pw5t' # BRASIL 
        # 'https://www.bbc.com/portuguese/topics/cvjp2jr0k9rt' # ECONOMIA
        # 'https://www.bbc.com/portuguese/topics/c340q430z4vt' # SAÚDE
        # 'https://www.bbc.com/portuguese/topics/cr50y580rjxt' # CIÊNCIA
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
        } """