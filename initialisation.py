import json
import broker.rabbitmq as rabbitmq
from fastapi.encoders import jsonable_encoder
from aio_pika import ExchangeType


async def initialise():
  payload = {
    "action": "initialize_app_and_roles",
    "data": {
      "application":{
        "name":"EVAL",
        "version": "1.0.1"
      },
      "role":{
        "admin":{"organization": 15, "template": 15, "evaluation": 15, "evaluation_template": 15, "evaluation_doc": 15, "category": 15, "requirement": 15, "member": 15 },
        "editor":{"template": 15, "evaluation": 15, "evaluation_template":6, "evaluation_doc": 3,"category":6, "member": 15 },
        "stakeholder":{"evaluation": 2, "category": 6, "evaluation_template": 6},
        "evaluator":{"evaluation": 2, "evaluation_doc": 6}
      }
    }
  }
  
  await rabbitmq.publish(
    payload=json.dumps(jsonable_encoder(payload)).encode(),
    exchange_name="gdmp-authorization",
    exchange_type=ExchangeType.DIRECT,
    routing_key="initialize_project"
  )