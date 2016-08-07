from smartinvestplus_data_spider import CRAWLER_OBJ_GRAPH
from smartinvestplus_data_spider.pipelines.mongo_dao import MongoDao


class CloseRatesMongoPipeline(object):
    BRVM = 'BRVM'

    def __init__(self):
        self.mongo_dao = CRAWLER_OBJ_GRAPH.provide(MongoDao)

    def process_item(self, close_rates, spider):
        close_rate_date = close_rates['date']
        for close_rate in close_rates['close_rates']:
            self.mongo_dao.upsert_security(close_rate)
            self.mongo_dao.upsert_close_rate(close_rate_date, close_rate)
        self.mongo_dao.insert_scraped_close_rate_date(close_rate_date)
        return close_rates
