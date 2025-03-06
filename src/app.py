import uvicorn
from fastapi import FastAPI

from src.di.container import container
from src.routes import routers
from src.utils.logger import logger
from utils.lifespan_events import shutdown, startup


async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


def register_routers(app: FastAPI):
    for router in routers:
        app.include_router(router)


def create_app() -> FastAPI:
    logger.info('Inicializando a aplicação...')
    container.db_connection()
    app = FastAPI(
        title='Meu App',
        description='Documentação da API',
        version='1.0.0',
        lifespan=lifespan,
    )
    register_routers(app)
    return app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
