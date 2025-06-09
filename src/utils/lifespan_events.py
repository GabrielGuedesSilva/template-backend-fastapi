from src.background.scheduler import scheduler
from src.utils.logger import logger


async def startup():
    logger.info('Inicializando a aplicação...')
    scheduler.start()


async def shutdown():
    scheduler.shutdown()
    logger.info('Encerrando a aplicação...')
