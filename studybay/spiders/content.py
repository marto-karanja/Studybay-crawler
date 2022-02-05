import scrapy
import mysql.connector
import csv
import socket
import datetime
from scrapy.http import Request
from itemloaders.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from studybay.items import ContentItem

class StudyBayContent(scrapy.Spider):
    """Study Daddy connection harvestor"""
    name = "studybay_content"
    custom_settings = {
        'DOWNLOAD_DELAY' : '5',
        'AUTOTHROTTLE_ENABLED':'True',
        'AUTOTHROTTLE_START_DELAY':'2.0',
        'AUTOTHROTTLE_MAX_DELAY':'50.0',
        'AUTOTHROTTLE_TARGET_CONCURRENCY':'1',
        'AUTOTHROTTLE_DEBUG': 'True',
        'HTTPCACHE_ENABLED': 'False',
        'ITEM_PIPELINES':{
            'studybay.pipelines.content_db.ContentWriter': 700,
            },
    }
    #category = ['economics-homework-help']

    def start_requests(self):
        links = set()
        # open database connection and fetch links
        conn = mysql.connector.connect(user='kush', passwd='incorrect', db='crawls', host='localhost', charset="utf8", use_unicode=True)
        cursor = conn.cursor()
        cursor.execute("SELECT link_no, link, category FROM studybay_links where processed='False' order by rand();")
        rows = cursor.fetchall()
        conn.close()
        self.logger.info('%s urls fetched', len(rows))

        #iterate through the links
        for link_no,link, category in rows:
            link = 'https://studybay.com' + link
            yield scrapy.Request(link, meta={"link_no": link_no, "category": category}, headers = {'referer': 'https://www.google.com/' }, callback = self.parse_content)

    def parse_content(self, response):
        
        loader = ItemLoader(item=ContentItem(), response = response)

        # extract content

        # extract content
        content =response.css(".project-example__concise-text").css(".p::text").extract()
        cleaned_content = content[-1]
        loader.add_value('content', cleaned_content )


        title = cleaned_content[0:60] + "..."
        loader.add_value('title', title)
        #add category
        loader.add_value('category', response.meta['category'])
        # add link no
        loader.add_value('link_no', response.meta['link_no'])
        #add housekeeping
        loader.add_value('project', self.settings.get('BOT_NAME'))
        loader.add_value('spider', self.name)
        loader.add_value('server', socket.gethostname())
        loader.add_value('date', datetime.datetime.now())

        yield loader.load_item()

        


        