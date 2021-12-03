from enum import Enum
from math import floor

from .config import Config
from .logger import Logger

from binance import Client
from binance.exceptions import BinanceAPIException
# from .binanceStreamer import BinanceStreamer


class OrderAction(Enum):
    BUY = 1
    SELL = 2


class BinanceAPI:
    def __init__(self, stream=None, database=None):
        config = Config()
        self.logger = Logger(service='BinanceAPI',
                             stream=stream,
                             database=database)

        self.client = Client(testnet=config.testnet,
                             api_key=config.testnet_api_key
                             if config.testnet else
                             config.api_key,
                             api_secret=config.testnet_secret_key
                             if config.testnet else
                             config.secret_key,
                             tld=config.tld)

        # self.streamer = BinanceStreamer(config)

    def get_account(self):
        return self.client.get_account()

    def get_ticker_price(self, ticker):
        """ FETCH FROM STREAMER BUFFER """
        return self.client.get_symbol_ticker(ticker)

    def get_currency_balance(self, currency):
        """ FETCH FROM STREAMER BUFFER """
        for balance in self.get_account()['balances']:
            if balance['asset'] == currency:
                return float(balance['free'])
        return None

    def __get_symbol_filter(self, ticker, filter_name):
        for filter_obj in self.client.get_symbol_info(ticker)['filters']:
            if filter_obj['FilterType'] == filter_name:
                return filter_obj

    def __calculate_ticker_step_size(self, ticker):
        """ TO BE CACHED """
        return float(self.__get_symbol_filter(ticker, "LOT_SIZE")['stepSize'])

    def __calculate_quantity(self, ticker, balance):
        """
        Format quantity to correct lot size.
        """
        ticker_price = self.get_ticker_price(ticker)    # put on stream
        step_size = self.__calculate_ticker_step_size(ticker)
        return floor(balance * step_size / ticker_price) / step_size

    def place_order(self,
                    base_currency,
                    quote_currency,
                    action):
        """
        Placing order of specified type.
        :param action: OrderAction
        :return: order confirmation details
        """
        log_msg_prefix = f'{action} {base_currency}->{quote_currency}'

        op_currency = base_currency if action == OrderAction.SELL else quote_currency
        op_balance = self.get_currency_balance(op_currency)

        self.logger.info(log_msg_prefix + f'Balance {op_balance}{op_currency}')

        calculated_quantity = self.__calculate_quantity(base_currency + quote_currency,
                                                        op_balance)

        self.logger.info(log_msg_prefix + f'{calculated_quantity}{op_currency} will be placed')
