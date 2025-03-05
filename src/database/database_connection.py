from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DatabaseConnection:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.session = self.get_session()

    def get_session(self):
        with Session(self.engine) as session:
            return session
