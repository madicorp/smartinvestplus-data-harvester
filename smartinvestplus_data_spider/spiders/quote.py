import json

import scrapy


class Quote(scrapy.Item):
    security_code = scrapy.Field()
    security_label = scrapy.Field()
    previous_quote = scrapy.Field()
    current_quote = scrapy.Field()
    exchanged_volume = scrapy.Field()
    transactions_nb = scrapy.Field()
    exchanged_value = scrapy.Field()


class Quotes(scrapy.Item):
    date = scrapy.Field()
    quotes = scrapy.Field()


class QuoteEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Quote):
            return dict(obj)
        return json.JSONEncoder.default(self, obj)


class QuotesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Quotes):
            return {'date': obj.date, 'quotes': [QuoteEncoder().default(quote) for quote in obj.quotes]}
        return json.JSONEncoder.default(self, obj)
