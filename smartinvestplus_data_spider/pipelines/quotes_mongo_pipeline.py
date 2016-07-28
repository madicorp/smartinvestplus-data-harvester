from pymongo import MongoClient


class QuotesMongoPipeline(object):
    BRVM = 'BRVM'

    def __init__(self):
        self.db = MongoClient()['smartinvestplustest']
        self.stock_exchanges = self.db['stock_exchange']

    def process_item(self, quotes, spider):
        quote_date = quotes['date']
        # TODO Handle element failure. Do not crash all and report it
        for quote in quotes['quotes']:
            self._upsert_security(quote)
            self._insert_quote(quote_date, quote)
        return quotes

    def _upsert_security(self, quote):
        pass
        security_code = quote['security_code'].upper()
        query = {'_id': self.BRVM, 'securities._id': security_code}
        print 'security', security_code, self.stock_exchanges.find(query).count()
        for stock_exchange in self.stock_exchanges.find(query):
            print 'stock_exchange', stock_exchange
        if self.stock_exchanges.find(query).count() > 0:
            update_to_perform = {'$set': {'securities.$.name': quote['security_label']}}
            self.stock_exchanges.update_one(query, update_to_perform)
        else:
            query = {'_id': self.BRVM}
            update_to_perform = {'$push': {'securities': {'_id': security_code, 'name': quote['security_label']}}}
            self.stock_exchanges.update_one(query, update_to_perform)

    def _insert_quote(self, quote_date, quote):
        pass
        query = {'stock_exchange': self.BRVM, 'security': quote['security_code'].lower()}
        update_to_perform = {'$set': {'rate': quote['current_quote'].lower(), 'date': quote_date, 'generated': False}}
        self.db['close_rates'].update_one(query, update_to_perform, True)
