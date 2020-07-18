import scrapy
import requests
import geocoder

import mysql.connector as mysql

from scrapy import Request
from pypika import Table, Query
from urllib.parse import urljoin
from sharkCrawler import settings

db = mysql.connect(host='127.0.0.1',
                   user=settings.DB_USER,
                   password=settings.DB_PASSWD,
                   database=settings.DB_NAME)
cursor = db.cursor()

class StoreGetSpider(scrapy.Spider):
    name = 'StoreGet'
    start_urls = [
        "https://www.foodpanda.com.tw/"
    ]

    def parse(self, response):
        cities = response.xpath('//*[@class="city-tile"]/@href').extract()
        fp_url = self.settings.get('FOODPANDA_URL')

        for city in cities:
            city_url = urljoin(fp_url, city)

            yield Request(url=city_url, callback=self.parse_store)

    def parse_store(self, response):
        stores = response.xpath('//*[@class="hreview-aggregate url"]/@href').extract()
        fp_url = self.settings.get('FOODPANDA_URL')

        for store in stores:
            store_url = urljoin(fp_url, store)
            
            yield Request(url=store_url, callback=self.parse_information)
    
    def parse_information(self, response):
        name = response.xpath('//*[@class="vendor-name"]/text()').get()
        address = response.xpath('//*[@class="vendor-location"]/text()').get()
        image = response.xpath('//*[starts-with(@class, "b-lazy")]/@data-src').get().split('|')[0].split('?')[0]
        location = geocoder.arcgis(address).latlng
        lot = location[1]
        lat = location[0]
        url = urljoin(self.settings.get('API_URL'), 'store/add')
        data = {
            'name': name,
            'address': address,
            'rating': 0,
            'latitude': lat,
            'longitude': lot,
            'image': image
        }

        requests.post(url=url, data=data)