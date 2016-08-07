from smartinvestplus_data_spider.pipelines.parser import Parser


class QuotesParsePipeline(object):
    def process_item(self, quotes, spider):
        return self._parse_quotes(quotes)

    @staticmethod
    def _parse_quotes(quotes):
        quotes['date'] = Parser.parse_to_date(quotes['date'])
        quotes['quotes'] = [QuotesParsePipeline._parse_quote(quote) for quote in quotes['quotes']]
        return quotes

    @staticmethod
    def _parse_quote(quote):
        fields = ['previous_quote', 'current_quote', 'current_quote', 'exchanged_volume', 'transactions_nb',
                  'exchanged_value']
        for field in fields:
            QuotesParsePipeline._field_to_float(quote, field)
        return quote

    @staticmethod
    def _field_to_float(quote, field_name):
        quote[field_name] = float(quote[field_name])
