"""
    Configuration object for BinanceWrapper class.
    Parses defined by the user
"""

import os
import configparser

CONFIG_FILE_NAME = '.BinanceWrapper.ini'
CONFIG_SECTION_NAME = 'BINANCE_METADATA'

class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_NAME)
        parseConfig = lambda x: config.get(CONFIG_SECTION_NAME, x)

        # Testnet option
        self.testnet = True if parseConfig('TESTNET') == 'TRUE' else False
        self.testnet_api_key = os.environ.get('TestnetApiKey') or parseConfig('TESTNET_API_KEY')
        if self.testnet is True and self.testnet_api_key is None:
            raise ValueError(
                'Testnet option specified but API Key is not provided. Please put into environmental variable TestnetApiKey or put into .BinanceWrapper.ini file')
        self.testnet_secret_key = os.environ.get('TestnetSecretKey') or parseConfig('TESTNET_SECRET_KEY')
        if self.testnet is True and self.testnet_secret_key is None:
            raise ValueError(
                'Testnet option specified but Secret Key is not provided. Please put into environmental variable TestnetSecretKey or put into .BinanceWrapper.ini file')

        # API Key
        self.api_key = os.environ.get('BinanceApiKey') or parseConfig('BINANCE_API_KEY')
        if self.testnet is False and self.api_key is None:
            raise ValueError('Binance API key is not provided! Please put into environmental variable BinanceApiKey or put into .BinanceWrapper.ini file')

        # Secret Key
        self.secret_key = os.environ.get('BinanceSecretKey') or parseConfig('BINANCE_SECRET_KEY')
        if self.secret_key is None:
            raise ValueError('Binance secret key is not provided! Please put into environmental variable BinanceSecretKey or put into .BinanceWrapper.ini file')

        # TLD
        self.tld = parseConfig('TLD')

        # Timeouts
        self.sell_timeout = parseConfig('SELL_TIMEOUT')
        self.buy_timeout = parseConfig('BUY_TIMEOUT')
