import logging
from datetime import datetime
from config import config

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('BCI_System')
        self.logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        # File handler
        file_handler = logging.FileHandler(config.LOG_FILE)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_formatter)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

logger = Logger()
