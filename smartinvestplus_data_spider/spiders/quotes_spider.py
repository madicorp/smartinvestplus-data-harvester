import scrapy
from quote import Quotes
from quote_loader import QuoteLoader
from scrapy.selector import Selector


class TodayQuotesSpider(scrapy.Spider):
    name = 'today_quotes_spider'
    start_urls = ['http://bfin.brvm.org/default.aspx']

    def parse(self, response):
        extracted_quotes = []
        for quote_html in self._extract_quotes(response):
            extracted_quotes.append(self._parse_quote(quote_html))
        quote_date = self._extract_quote_date(response)
        quotes = Quotes(date=quote_date, quotes=extracted_quotes)
        yield quotes

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

    @staticmethod
    def _extract_quote_date(response):
        return response.xpath('//select[@id="ctl00_Main_DropDownList1"]/option[@selected]/@value').extract_first()
