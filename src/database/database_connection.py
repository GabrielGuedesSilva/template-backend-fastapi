import time

from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from src.utils.logger import logger


class DatabaseConnection:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.session = self.get_session()

    def get_session(self):
        try:
            with Session(self.engine) as session:
                return session
        except Exception as error:
            logger.error(f'Erro ao acessar session: {str(error)}')
            raise HTTPException(
                status_code=500, detail='Erro ao acessar o banco de dados.'
            )

    def check_connection(self, max_retries=1, delay=6):
        attempts = 0
        result = False
        logger.info('Tentando conectar ao banco de dados...')
        while attempts < max_retries:
            try:
                self.session.execute(text('SELECT 1'))
                logger.info('Conexão com o banco de dados bem-sucedida.')
                result = True
                return result
            except Exception as error:
                attempts += 1
                result = False
                time.sleep(delay)
                logger.error(
                    f'Erro ao tentar conectar ao banco de dados: {str(error)}'
                )
        if not result:
            raise ConnectionError(
                'O banco de dados está temporariamente indisponível.'
            )
