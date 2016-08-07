from smartinvestplus_data_spider.pipelines.parser import Parser


class CloseRatesParsePipeline(object):
    def process_item(self, close_rates, spider):
        return self._parse_close_rates(close_rates)

    @staticmethod
    def _parse_close_rates(close_rates):
        close_rates['date'] = Parser.parse_to_date(close_rates['date'])
        close_rates['close_rates'] = \
            [CloseRatesParsePipeline._parse_close_rate(close_rate) for close_rate in close_rates['close_rates']]
        return close_rates

    @staticmethod
    def _parse_close_rate(close_rate):
        fields = ['previous_close_rate', 'current_close_rate', 'exchanged_volume', 'transactions_nb',
                  'exchanged_value']
        for field in fields:
            CloseRatesParsePipeline._field_to_float(close_rate, field)
        return close_rate

    @staticmethod
    def _field_to_float(close_rate, field_name):
        close_rate[field_name] = float(close_rate[field_name])
