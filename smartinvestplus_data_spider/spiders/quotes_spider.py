import scrapy
from quote import Quotes
from quote_loader import QuoteLoader
from scrapy.selector import Selector
from smartinvestplus_data_spider import CRAWLER_OBJ_GRAPH
from smartinvestplus_data_spider.pipelines.mongo_dao import MongoDao
from smartinvestplus_data_spider.pipelines.parser import Parser


class QuotesSpider(scrapy.Spider):
    name = 'quotes_spider'
    brvm_url = 'http://bfin.brvm.org/default.aspx'
    start_urls = [brvm_url]

    def parse(self, response):
        self._extract_quotes_dates(response)
        quote_date = self.quotes_dates.pop()
        extracted_quotes = []
        for quote_html in QuotesSpider._extract_quotes(response):
            extracted_quotes.append(QuotesSpider._parse_quote(quote_html))
        quotes = Quotes(date=quote_date, quotes=extracted_quotes)
        yield quotes
        if not self.quotes_dates:
            return
        yield self.previous_quote_query(response)

    def previous_quote_query(self, response):
        previous_quote_date = self.quotes_dates[-1]
        form_data = {
            '__EVENTTARGET': 'ctl00$Main$DropDownList1',
            'ctl00$Main$DropDownList1': previous_quote_date
        }
        return scrapy.FormRequest.from_response(response=response, formdata=form_data)

    @staticmethod
    def _parse_quote(quote_html):
        quote_elements_selector = Selector(text=quote_html).css(':root')
        quote_loader = QuoteLoader(selector=quote_elements_selector)
        return quote_loader.parse_quote()
        # Quote line sample HTML structure
        # <tr class="FreezingCol" align="center" bgcolor="White">
        #   <td>
        #       <font color="#003063" size="1">
        #           <img id="ctl00_Main_GridView1_ctl35_Image2"
        #                src="App_Themes/Default/Images/more.gif" border="0">
        #       </font>
        #   </td>
        #   <td align="left">
        #       <font color="#003063" size="1">UNXC</font>
        #   </td>
        #   <td align="left">
        #       <font color="#003063" size="1">UNIWAX CI</font>
        #   </td>
        #   <td align="right">
        #       <font color="#003063" size="1">  23 500</font>
        #   </td>
        #   <td align="right">
        #       <font color="Green" size="1"><b>  23 700</b></font></td>
        #   <td align="right">
        #       <font color="#003063" size="1">   101</font>
        #   </td>
        #   <td>
        #       <font color="#003063" size="1">   8</font>
        #   </td>
        #   <td align="right">
        #       <font color="#003063" size="1">  2 512 900</font>
        #   </td>
        # </tr>

    @staticmethod
    def _extract_quotes(response):
        return response.css('#ctl00_Main_GridView1 tr.FreezingCol').extract()

    def _extract_quotes_dates(self, response):
        if hasattr(self, 'quotes_dates'):
            return
        # Quotes dates has not been yet extracted
        quotes_dates = response.xpath('//select[@id="ctl00_Main_DropDownList1"]/option/@value').extract()
        mongo_dao = CRAWLER_OBJ_GRAPH.provide(MongoDao)
        quotes_dates_in_db = [Parser.format_date(quote_date) for quote_date in (mongo_dao.get_scraped_quotes_dates())]
        self.quotes_dates = [quote_date for quote_date in quotes_dates if quote_date not in quotes_dates_in_db]
        self.quotes_dates = sorted(self.quotes_dates, key=Parser.parse_to_date, reverse=True)
        self.quotes_dates = self.quotes_dates[:5]
