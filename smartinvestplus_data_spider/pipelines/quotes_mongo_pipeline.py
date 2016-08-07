from smartinvestplus_data_spider import CRAWLER_OBJ_GRAPH
from smartinvestplus_data_spider.pipelines.mongo_dao import MongoDao


class QuotesMongoPipeline(object):
    BRVM = 'BRVM'

    def __init__(self):
        self.mongo_dao = CRAWLER_OBJ_GRAPH.provide(MongoDao)

    def process_item(self, quotes, spider):
        quote_date = quotes['date']
        for quote in quotes['quotes']:
            self.mongo_dao.upsert_security(quote)
            self.mongo_dao.upsert_quote(quote_date, quote)
        self.mongo_dao.insert_scraped_close_rate_date(quote_date)
        return quotes
