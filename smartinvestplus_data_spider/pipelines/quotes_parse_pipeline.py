import datetime


class QuotesParsePipeline(object):
    def process_item(self, quotes, spider):
        return self._parse_quotes(quotes)

    def _parse_quotes(self, quotes):
        quotes['date'] = datetime.datetime.strptime(quotes['date'], '%Y%m%d')
        quotes['quotes'] = [self._parse_quote(quote) for quote in quotes['quotes']]
        return quotes

    def _parse_quote(self, quote):
        fields = ['previous_quote', 'current_quote', 'current_quote', 'exchanged_volume', 'transactions_nb',
                  'exchanged_value']
        for field in fields:
            self._field_to_float(quote, field)
        return quote

    def _field_to_float(self, quote, field_name):
        quote[field_name] = float(quote[field_name])
