from pymongo import MongoClient


class MongoDao(object):
    BRVM = 'BRVM'

    def __init__(self):
        self.db = MongoClient()['smartinvestplus']
        self.stock_exchanges = self.db['stock_exchanges']
        self.close_rates = self.db['close_rates']
        self.scraped_close_rate_dates = self.db['scraped_close_rate_dates']

    def upsert_security(self, quote):
        security_code = quote['security_code'].upper()
        query = {'_id': self.BRVM, 'securities._id': security_code}
        security_label = quote['security_label']
        if self.stock_exchanges.find(query).count() > 0:
            update_to_perform = {'$set': {'securities.$.name': security_label}}
            self.stock_exchanges.update_one(query, update_to_perform)
        else:
            query = {'_id': self.BRVM}
            update_to_perform = {'$push': {'securities': {'_id': security_code, 'name': security_label}}}
            self.stock_exchanges.update_one(query, update_to_perform)

    def upsert_quote(self, quote_date, quote):
        query = {'stock_exchange': self.BRVM, 'security': quote['security_code'].upper()}
        update_to_perform = {'$set': {'rate': quote['current_quote'], 'date': quote_date, 'generated': False}}
        self.close_rates.update_one(query, update_to_perform, True)

    def get_scraped_quotes_dates(self):
        return self.scraped_close_rate_dates.distinct('date')

    def insert_scraped_close_rate_date(self, scraped_quote_date):
        return self.scraped_close_rate_dates.insert({'date': scraped_quote_date})
