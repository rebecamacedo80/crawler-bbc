import scrapy
import pandas as pd
import re

class G1Spider(scrapy.Spider):
    name = "terra"
    def start_requests(self):        
        urls = []        
        df = pd.read_csv('/home/rebeca/LinksNotícias/linksExtraídosTERRA-ESPORTES/merge_linksTEsportes.csv', sep=';')

        for index, row in df.iterrows():
            link = row['links']
            urls.append('http://'+link)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):               
        text =  response.css("div.colMain")

        if text != None:
            title =  text.css("div.title.headline h1::text").get()
            sub = text.css("div.articleData p.text").get()
            subtitle = re.sub('\t|\n|<[^>]*>', '', str(sub))

            if title != None and subtitle != None:
                if len(title) > len(subtitle):
                    pass
                else:
                    yield{
                        'title': title,
                        'subtitle': subtitle
                    }

        elif response.css("div.main-content") != None:            
            title = response.css("div.main-content div.content-section h1::text").get()
            sub = response.css("div.main-content div.content-section.content p").get()
            subtitle = re.sub('\t|\n|<[^>]*>', '', str(sub))

            if title != None and subtitle != None:
                if len(title) > len(subtitle):
                    pass
                else:
                    yield{
                        'title': title,
                        'subtitle': subtitle
                    }