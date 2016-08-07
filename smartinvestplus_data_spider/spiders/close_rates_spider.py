import scrapy
from close_rate import CloseRates
from close_rate_loader import CloseRatesLoader
from scrapy.selector import Selector
from smartinvestplus_data_spider import CRAWLER_OBJ_GRAPH
from smartinvestplus_data_spider.pipelines.mongo_dao import MongoDao
from smartinvestplus_data_spider.pipelines.parser import Parser


class CloseRatesSpider(scrapy.Spider):
    name = 'close_rates_spider'
    brvm_url = 'http://bfin.brvm.org/default.aspx'
    start_urls = [brvm_url]

    def parse(self, response):
        if not hasattr(self, 'close_rates_dates'):
            self._extract_close_rates_dates(response)
            yield self._next_close_rate_request(response)
        else:
            close_rate_date = self.close_rates_dates.pop()
            extracted_close_rates = []
            for close_rate_html in CloseRatesSpider._extract_close_rates(response):
                extracted_close_rates.append(CloseRatesSpider._parse_close_rate(close_rate_html))
            close_rates = CloseRates(date=close_rate_date, close_rates=extracted_close_rates)
            yield close_rates
            if not self.close_rates_dates:
                # No more close rate to process
                return
            yield self._next_close_rate_request(response)

    def _next_close_rate_request(self, response):
        close_rate_date = self.close_rates_dates[-1]
        print 'building post for', close_rate_date
        form_data = {
            '__EVENTTARGET': 'ctl00$Main$DropDownList1',
            'ctl00$Main$DropDownList1': close_rate_date
        }
        return scrapy.FormRequest.from_response(response=response, formdata=form_data)

    @staticmethod
    def _parse_close_rate(close_rate_html):
        close_rate_elements_selector = Selector(text=close_rate_html).css(':root')
        close_rates_loader = CloseRatesLoader(selector=close_rate_elements_selector)
        return close_rates_loader.parse_close_rate()
        # Close rate line sample HTML structure
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
    def _extract_close_rates(response):
        return response.css('#ctl00_Main_GridView1 tr.FreezingCol').extract()

    def _extract_close_rates_dates(self, response):
        close_rates_dates = response.xpath('//select[@id="ctl00_Main_DropDownList1"]/option/@value').extract()
        mongo_dao = CRAWLER_OBJ_GRAPH.provide(MongoDao)
        close_rates_in_db = \
            [Parser.format_date(close_rate_date) for close_rate_date in (mongo_dao.get_scraped_close_rate_dates())]
        self.close_rates_dates = \
            [close_rate_date for close_rate_date in close_rates_dates if close_rate_date not in close_rates_in_db]
        self.close_rates_dates = sorted(self.close_rates_dates, key=Parser.parse_to_date)
