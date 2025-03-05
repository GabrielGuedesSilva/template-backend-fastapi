from http import HTTPStatus
from fastapi import FastAPI
from src.routes.users import router as users_router

app = FastAPI()
app.include_router(users_router)


@app.get('/', status_code=HTTPStatus.OK)
def root():
    return {'Message': 'Hello World'}