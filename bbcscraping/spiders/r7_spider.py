import scrapy
import pandas as pd
import re

class G1Spider(scrapy.Spider):
    name = "r7"
    def start_requests(self):        
        urls = []        
        df = pd.read_csv('/home/rebeca/LinksNotícias/linksExtraídosR7/links2019.csv', sep=';')

        for index, row in df.iterrows():
            link = row['links']
            urls.append('http://'+link)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        text = response.css("header div.heading-title")
        title = text.css("h1::text").get()
        subtitle = text.css("h2::text").get()

        if title != None and subtitle != None:

            yield{
                'title': title.strip(),
                'subtitle': subtitle.strip()
            }