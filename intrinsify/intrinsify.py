import sys                      
import pandas as pd
import click
from iexfinance import Stock
from iexfinance import get_historical_data
from iexfinance import get_market_tops
from iexfinance import get_stats_intraday
from money import Money
from tabulate import tabulate

def format_num_to_currency(num):
    return Money(num, 'USD').format('en_US')

def float_to_percentage_string(num):
    return '{:.2f}%'.format(float(num))

def format_result_string(*args):
    return '  |  '.join(args)

def print_stock_data(ticker):
    data = StockData(ticker)
    print(data)

@click.command()
def intrinsify():
    data = StockData('KO')
    print(data)

class StockData():
    data_headers = ['Name',
        'Ticker',
        'Price',
        'Flat Growth Estimate',
        'AAA Corp Bond Yield',
        'EPS',
        'Intrinsic Value',
        'Normalized IV']

    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = Stock(ticker, output_format='pandas')
        self.name = self.stock.get_company_name()['companyName'].to_string()
        self.price = self.stock.get_price()['price'][ticker]
        self.eps = self.stock.get_key_stats()[ticker]['latestEPS']
        self.flat_growth_estimate = 5
        self.aaa_corporate_bond_yield = 3.56
        self.intrinsic_value = (self.eps * (8.5 + (2 * self.flat_growth_estimate)) * 4.4) \
            / self.aaa_corporate_bond_yield
        self.norm_intrinsic_value = self.intrinsic_value / self.price

    def construct_tabular_output(self):
        return [[self.name,
                 self.ticker.upper(),
                 format_num_to_currency(self.price),
                 float_to_percentage_string(self.flat_growth_estimate),
                 float_to_percentage_string(self.aaa_corporate_bond_yield),
                 format_num_to_currency(self.eps),
                 format_num_to_currency(self.intrinsic_value),
                 '{:.2f}'.format(self.norm_intrinsic_value)]]

    def __str__(self):
        return tabulate(self.construct_tabular_output(), self.data_headers)

if __name__ == '__main__':
    intrinsify()