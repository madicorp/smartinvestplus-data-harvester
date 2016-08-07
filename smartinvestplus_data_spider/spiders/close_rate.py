import json

import scrapy


class CloseRate(scrapy.Item):
    security_code = scrapy.Field()
    security_label = scrapy.Field()
    previous_close_rate = scrapy.Field()
    current_close_rate = scrapy.Field()
    exchanged_volume = scrapy.Field()
    transactions_nb = scrapy.Field()
    exchanged_value = scrapy.Field()


class CloseRates(scrapy.Item):
    date = scrapy.Field()
    close_rates = scrapy.Field()


class CloseRateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CloseRate):
            return dict(obj)
        return json.JSONEncoder.default(self, obj)


class CloseRatesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CloseRates):
            return {
                'date': obj.date,
                'close_rates': [CloseRateEncoder().default(close_rate) for close_rate in obj.close_rates]
            }
        return json.JSONEncoder.default(self, obj)
