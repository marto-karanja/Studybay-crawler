import datetime
import csv
import os
import sys
import scrapy
import datetime

from scrapy import Request
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from studybay.items import LinkItem



class StudybayLink(scrapy.Spider):
    name="studybay_links"

    custom_settings = {
        'DOWNLOAD_DELAY' : '5',
        'AUTOTHROTTLE_ENABLED':'True',
        'AUTOTHROTTLE_START_DELAY':'2.0',
        'AUTOTHROTTLE_MAX_DELAY':'36.0',
        'AUTOTHROTTLE_TARGET_CONCURRENCY':'1',
        'AUTOTHROTTLE_DEBUG': 'True',
        'HTTPCACHE_ENABLED': 'True',
        'ITEM_PIPELINES':{
            'studybay.pipelines.link_db.LinkSaver': 700,
            },
        
    }

    

    #=----------------------------------------------------------------
    def start_requests(self):
        start_urls = [
            'https://studybay.com/latest-orders/english-language/', 'https://studybay.com/latest-orders/business/',        
            'https://studybay.com/latest-orders/psychology/',      
            'https://studybay.com/latest-orders/history/',
            'https://studybay.com/latest-orders/nursing/',
            'https://studybay.com/latest-orders/management/',      
            'https://studybay.com/latest-orders/health-care/',     
            'https://studybay.com/latest-orders/sociology/',       
            'https://studybay.com/latest-orders/literature/',      
            'https://studybay.com/latest-orders/education/',       
            'https://studybay.com/latest-orders/politics/',        
            'https://studybay.com/latest-orders/economics/',       
            'https://studybay.com/latest-orders/marketing/',       
            'https://studybay.com/latest-orders/philosophy/',      
            'https://studybay.com/latest-orders/criminology/',     
            'https://studybay.com/latest-orders/law/',
            'https://studybay.com/latest-orders/arts/',
            'https://studybay.com/latest-orders/religion/',        
            'https://studybay.com/latest-orders/communications/',  
            'https://studybay.com/latest-orders/information-technology/',
            'https://studybay.com/latest-orders/biology/',
            'https://studybay.com/latest-orders/social-work/',     
            'https://studybay.com/latest-orders/accounting/',      
            'https://studybay.com/latest-orders/computer-science/', 'https://studybay.com/latest-orders/cultural-studies/', 'https://studybay.com/latest-orders/finance/',
            'https://studybay.com/latest-orders/environmental-sciences/',
            'https://studybay.com/latest-orders/medical/',
            'https://studybay.com/latest-orders/engineering/',     
            'https://studybay.com/latest-orders/statistics/',      
            'https://studybay.com/latest-orders/technology/',      
            'https://studybay.com/latest-orders/project-management/',
            'https://studybay.com/latest-orders/anthropology/',    
            'https://studybay.com/latest-orders/music/',
            'https://studybay.com/latest-orders/film/',
            'https://studybay.com/latest-orders/mathematics/',     
            'https://studybay.com/latest-orders/media/',
            'https://studybay.com/latest-orders/human-geography/', 
            'https://studybay.com/latest-orders/chemistry/',       
            'https://studybay.com/latest-orders/human-rights/',    
            'https://studybay.com/latest-orders/public-relations/', 'https://studybay.com/latest-orders/sports/',
            'https://studybay.com/latest-orders/journalism/',      
            'https://studybay.com/latest-orders/tourism/',
            'https://studybay.com/latest-orders/childcare/',       
            'https://studybay.com/latest-orders/employment/',      
            'https://studybay.com/latest-orders/architecture/',    
            'https://studybay.com/latest-orders/linguistics/',     
            'https://studybay.com/latest-orders/physics/',
            'https://studybay.com/latest-orders/astronomy/',       
            'https://studybay.com/latest-orders/physical-education/',
            'https://studybay.com/latest-orders/geology/',
            'https://studybay.com/latest-orders/fashion/',
            'https://studybay.com/latest-orders/construction/',    
            'https://studybay.com/latest-orders/money-and-banking/',
            'https://studybay.com/latest-orders/archaeology/',     
            'https://studybay.com/latest-orders/health/',
            'https://studybay.com/latest-orders/geography/',       
            'https://studybay.com/latest-orders/reports/',
            'https://studybay.com/latest-orders/research-paper/',  
            'https://studybay.com/latest-orders/paraphrasing/',    
            'https://studybay.com/latest-orders/personal-statement/',
            'https://studybay.com/latest-orders/dissertation/',    
            'https://studybay.com/latest-orders/thesis-statement/', 'https://studybay.com/latest-orders/proofreading/',    
            'https://studybay.com/latest-orders/term-paper/',      
            'https://studybay.com/latest-orders/annotated-bibliography/',
            'https://studybay.com/latest-orders/essay/',
            'https://studybay.com/latest-orders/lab-report/',      
            'https://studybay.com/latest-orders/literature-movie-review/',
            'https://studybay.com/latest-orders/thesis/',
            'https://studybay.com/latest-orders/capstone-project/', 'https://studybay.com/latest-orders/model-answer-exam-revision/',
            'https://studybay.com/latest-orders/research-summary/', 'https://studybay.com/latest-orders/poetry-prose/',    
            'https://studybay.com/latest-orders/questions-answers/',
            'https://studybay.com/latest-orders/reflective-practice/',
            'https://studybay.com/latest-orders/content-writing/', 
            'https://studybay.com/latest-orders/dissertation-proposal/',
            'https://studybay.com/latest-orders/non-word-assignments/',
            'https://studybay.com/latest-orders/math-solving/',    
            'https://studybay.com/latest-orders/thesis-dissertation-chapter/',
            'https://studybay.com/latest-orders/case-study/',      
            'https://studybay.com/latest-orders/speech/',
            'https://studybay.com/latest-orders/coursework/',      
            'https://studybay.com/latest-orders/thesis-proposal/', 
            'https://studybay.com/latest-orders/powerpoint-presentation/',
            'https://studybay.com/latest-orders/research-proposal/',
            'https://studybay.com/latest-orders/speech-presentation/',
            'https://studybay.com/latest-orders/admission-scholarship-essay/',
            'https://studybay.com/latest-orders/outline/',
            'https://studybay.com/latest-orders/math-assignment/', 
            'https://studybay.com/latest-orders/business-plan/',   
            'https://studybay.com/latest-orders/creative-writing/'
            ]
        for url in start_urls:
            category = url.split("/")[-2]
            print(category)
            yield Request(url, meta={"category": category}, headers = {'referer': 'https://www.google.com/' }, callback = self.parse_links )

    #---------------------------------------------------------------------

    def parse_links(self, response):
        """extract page links"""
        links = response.css(".related-project__heading").css(".a").css("::attr(href)").extract()

        #use item loader to save in database
        loader = ItemLoader(item=LinkItem(), response=response)
        loader.add_value('links', links)
        loader.add_value('referring_link', response.url)
        loader.add_value('project', self.settings.get('BOT_NAME'))
        loader.add_value('spider', self.name)
        loader.add_value('date', datetime.datetime.now())
        loader.add_value('category', response.meta['category'])



        yield loader.load_item()

        # get page links
        links = response.css(".pagination__link").css("::attr(href)").extract()
        for count, link in enumerate(links):
            if response.urljoin(link) == response.url:
                if count + 1 <= len(links):
                    next_page = links[count + 1]
                    yield Request(response.urljoin(next_page), meta={"category": response.meta['category']}, headers = {'referer': 'https://www.google.com/' }, callback = self.parse_links )
                else:
                    # break out of loop
                    pass
        



