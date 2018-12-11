import sys
import pandas as pd
import click
from money import Money
from iexfinance import Stock
from iexfinance import get_historical_data
from iexfinance import get_market_tops
from iexfinance import get_stats_intraday
from tabulate import tabulate

data_headers = [
    'Y/N',
    'Name',
    'Ticker',
    'Price',
    'Flat Growth Estimate',
    'AAA Corp Bond Yield',
    'EPS',
    'Intrinsic Value',
    'Normalized IV'
]

@click.command()
# @click.argument('tickers', nargs=-1)
@click.argument('input', type=click.File('rb'), nargs=-1)
def intrinsify(input):
    click.echo("Parsing input file...")
    tickers = parse_file_input(input)

    click.echo("Fetching stock data...")
    stocks = [StockData(ticker) for ticker in tickers]

    stocks_tabular = [stock.construct_tabular_output() for stock in stocks]
    click.echo(tabulate(stocks_tabular, data_headers, tablefmt='psql'))

def parse_file_input(input):
    tickers = []
    for f in input:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            tickers += chunk.decode('utf-8').strip().replace(' ', '').split(',')

    return tickers

class StockData():
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = Stock(ticker, output_format='pandas')
        self.sector = self.stock.get_sector()['sector'][ticker]
        self.name = self.stock.get_company_name()['companyName'].to_string()
        self.price = self.stock.get_price()['price'][ticker]
        self.eps = self.stock.get_key_stats()[ticker]['latestEPS']
        self.flat_growth_estimate = 5
        self.aaa_corporate_bond_yield = 3.56
        self.intrinsic_value = (self.eps * (8.5 + (2 * self.flat_growth_estimate)) * 4.4) \
            / self.aaa_corporate_bond_yield
        self.norm_intrinsic_value = self.intrinsic_value / self.price
        self.attractive = u'\u2713' if self.norm_intrinsic_value > 1 else ' '

    def construct_tabular_output(self):
        return [
            self.attractive,
            self.name,
            self.ticker.upper(),
            num_to_currency(self.price),
            float_to_percentage_string(self.flat_growth_estimate),
            float_to_percentage_string(self.aaa_corporate_bond_yield),
            num_to_currency(self.eps),
            num_to_currency(self.intrinsic_value),
            pretty_float(self.norm_intrinsic_value)
        ]

    def to_dict(self):
        return {
            'Name': self.name,
            'Ticker': self.ticker.upper(),
            'Price': num_to_currency(self.price),
            'Flat Growth Estimate': float_to_percentage_string(self.flat_growth_estimate),
            'AAA Corp Bond Yield': float_to_percentage_string(self.aaa_corporate_bond_yield),
            'EPS': num_to_currency(self.eps),
            'Intrinsic Value': num_to_currency(self.intrinsic_value),
            'Normalized IV': pretty_float(self.norm_intrinsic_value)
        }

    def __str__(self):
        return tabulate([self.construct_tabular_output()], data_headers)

def num_to_currency(num):
    return Money(num, 'USD').format('en_US')

def float_to_percentage_string(num):
    return '{:.2f}%'.format(float(num))

def pretty_float(num):
    return "%.2f" % num

if __name__ == '__main__':
    intrinsify()
