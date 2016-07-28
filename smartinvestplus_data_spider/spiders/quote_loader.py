import unicodedata

import re
import scrapy
from quote import Quote
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


def _is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def _parse_to_primitive(value):
    value_without_spaces = re.sub('\s', '', value)
    if _is_number(value_without_spaces):
        return value_without_spaces
    return value


def _unicode_to_string(value):
    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')


class QuoteLoader(scrapy.loader.ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip, _parse_to_primitive, _unicode_to_string)
    default_output_processor = TakeFirst()

    def __init__(self, selector):
        super(QuoteLoader, self).__init__(item=Quote(), selector=selector)

    def parse_quote(self):
        _cell_selector = QuoteLoader._cell_selector
        _bold_cell_selector = QuoteLoader._bold_cell_selector
        self.add_css('security_code', _cell_selector(2))
        self.add_css('security_label', _cell_selector(3))
        self.add_css('previous_quote', _cell_selector(4))
        self.add_css('current_quote', _bold_cell_selector(5))
        self.add_css('exchanged_volume', _cell_selector(6))
        self.add_css('transactions_nb', _cell_selector(7))
        self.add_css('exchanged_value', _cell_selector(8))
        return self.load_item()

    @staticmethod
    def _cell_selector(idx):
        return 'tr>td:nth-child(%s)>font::text' % idx

    @staticmethod
    def _bold_cell_selector(idx):
        return 'tr>td:nth-child(%s)>font>b::text' % idx
