import logging

from loguru import logger

from data.config import DIR

logger.add(f'{DIR}/logs/app.log', format='[{time}] [{level}] [{file.name}:{line}]  {message}',
           level='DEBUG', compression='zip')


class NoParsingFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().find('TelegramNetworkError') or not record.getMessage().find(
            "Sleep for")


logging.getLogger('aiogram').addFilter(NoParsingFilter())
