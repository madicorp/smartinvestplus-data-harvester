import datetime


class Parser(object):
    DATE_FORMAT = '%Y%m%d'

    @staticmethod
    def parse_to_date(formatted_date):
        return datetime.datetime.strptime(formatted_date, Parser.DATE_FORMAT)

    @staticmethod
    def format_date(date):
        return date.strftime(Parser.DATE_FORMAT).decode("utf-8")
