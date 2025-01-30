# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sqlite3 

class MongoDBPipeline:
    collection_name = 'transcripts'
    
    def open_spider(self, spider): 
        self.client = pymongo.MongoClient("CONNECTION_STRING", server_api=ServerApi('1'), tlsCAFile=certifi.where())
        self.db = self.client['My_Database']

    def close_spider(self, spider): 
        self.client.close() 

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
    
class SQLitePipeline:
    collection_name = 'transcripts'
    
    def open_spider(self, spider): 
        self.connection = sqlite3.connect('transcripts.db')
        self.c = self.connection.cursor() 
        # query 
        try: 
            self.c.execute(''' 
                CREATE TABLE transcripts(
                    'title' TEXT
                    , 'plot' TEXT
                    , 'transcripts' TEXT
                    , 'url' TEXT
                    )

            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider): 
        self.connection.close() 

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO transcripts (title, plot, 'transcripts', url) VALUES(?,?,?,?)
        ''', ( 
            item.get('title'), 
            item.get('plot'),
            item.get('transcripts'),
            item.get('url'),
        ))
        self.connection.commit()
        return item
