import scrapy
import pandas as pd
import re

class G1Spider(scrapy.Spider):
    name = "g1"
    def start_requests(self):        
        urls = []        
        df = pd.read_csv('/home/rebeca/linksGSHOW.csv', sep=';')

        for index, row in df.iterrows():
            link = row['links']
            urls.append('http://'+link)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):                
        text = response.css("div#glb-materia")

        """ http://globoesporte.globo.com/blogs/especial-blog/brasil-mundial-fc/post/fa-mirim-se-despede-de-pato-no-villarreal-aqui-sempre-sera-sua-casa.html?utm_source=Twitter&utm_medium=Social&utm_content=Esporte&utm_campaign=globoesportecom

        text = response.css("article")
        title = response.css("article header h2").get() 
        subtitle response.css("article span.conteudo-post p:nth-child(3)").get() """
         
        if text != []:
            title = text.css("div.materia-titulo h1.entry-title::text").get()
            sub = text.css("div.materia-titulo h2::text").get()

            if title != None or sub != None:
                if len(title) > len(sub):
                    pass
                else:
                    yield{
                        'title': title,
                        'subtitle': sub
                    }
        
        else:
            text = response.css("main.mc-body.theme")

            title = text.css("div.row.content-head.non-featured div.title h1.content-head__title::text").get()
            sub = text.css("div.row.content-head.non-featured div.medium-centered.subtitle h2.content-head__subtitle::text").get() 

            if sub == None:
                if title == None:
                    pass
                
                else:
                    sub = text.css("div.mc-article-body article div.mc-column.content-text.active-extra-styles p.content-text__container").get()
                    subtitle = re.sub('<[^>]*>', '', str(sub))

                    if sub == None:
                        pass

                    else:
                        if len(title) > len(subtitle):
                            pass
                        else:
                            yield{
                                'title': title,
                                'subtitle': subtitle
                            }
            else:
                if len(title) > len(sub):
                    pass
                else:
                    yield{
                        'title': title,
                        'subtitle': sub
                    }