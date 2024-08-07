from fastapi_app import app
from base_utils.utils import Test
from initialisation import initialise
import database.mongodb as mongodb
import broker.rabbitmq as rabbitmq


@app.on_event("startup")
async def start_db():
  test = Test.test
  await mongodb.init(test)
  await rabbitmq.init()
  await initialise()
