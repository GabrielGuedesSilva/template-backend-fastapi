from src.di.container import container
from src.utils.logger import logger


async def startup():
    db_connection = container.db_connection()
    db_connection.check_connection()


async def shutdown():
    logger.info('A aplicação está sendo desligada.')
