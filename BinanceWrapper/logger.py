import logging
import os

class Logger:
    def __init__(self,  service='SpotTrading',
                        stream=None,
                        database=None):
        self.logger = logging.getLogger(f'{service}Log')
        log_file_name = f'logs/{service}.log'
        os.makedirs(os.path.dirname(log_file_name), exist_ok=True)
        # Init handlers
        handlers = [
            logging.FileHandler(filename=log_file_name,
                                mode='a',
                                encoding='utf-8'
                                ),
            # if stream not provided output to stderr
            logging.StreamHandler(stream=stream)
        ]
        for h in handlers:
            h.setLevel(logging.DEBUG),
            h.setFormatter('%(asctime)s %(levelname)s %(message)s')
            self.logger.addHandler(h)

    # def add_stream_logger(self):
    #     print('stop')

    def log(self, message, level="info"):
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "debug":
            self.logger.debug(message)

    def info(self, message):
        self.log(message)

    def warning(self, message):
        self.warning(message)

    def error(self, message):
        self.error(message)

    def debug(self, message):
        self.debug(message)