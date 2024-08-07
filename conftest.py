import asyncio

import pytest
# from utils.utils import Test
from base_utils.utils import Test
from initialisation import initialise
import database.mongodb as mongodb
from fastapi_app import app
from httpx import AsyncClient


Test.set_test(True)

@pytest.fixture(autouse=True, scope='session')
def event_loop():
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  yield loop
  loop.close()


@pytest.fixture(autouse=True, scope='session')
def client(event_loop):
  test = Test.test
  database, db_name = event_loop.run_until_complete(mongodb.init(test, event_loop))
  event_loop.run_until_complete(initialise())

  yield AsyncClient(app=app, base_url="http://localhost:8000")

  event_loop.run_until_complete(database.drop_database(db_name))