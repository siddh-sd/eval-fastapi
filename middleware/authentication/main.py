import re
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from base_utils.utils import create_response
import json
import broker.rabbitmq as rabbitmq
from fastapi.encoders import jsonable_encoder
from aio_pika import ExchangeType
from database.redis import redis_client
from error_types import convert_error_type
from config import REDIS_EXPIRE_MINUTES

class AuthorizationMiddleware(BaseHTTPMiddleware):
  def __init__(self, app: ASGIApp, skip_endpoints: list = []) -> None:
    super().__init__(app, self.dispatch)
    self.url = "/api/v2"
    self.skip_endpoints = skip_endpoints
    
    
  async def dispatch(self, request: Request, call_next):
    endpoint = str(request.url)[len(str(request.base_url))-1:]

    if endpoint[:len(self.url)] == self.url:
      endpoint = endpoint[len(self.url):]
    

    for skip in self.skip_endpoints:
      if request.method == skip["method"] and re.search(skip["regex"], endpoint):
        return await call_next(request)
    

    if "authorization" in request.headers and "application" in request.headers and \
      "organization" in request.headers and "Bearer" in request.headers["authorization"]:
      token = request.headers["authorization"].split(" ")[-1]

      r_client = await redis_client()
      try:
        user_data = r_client[token]
      except Exception:
        payload = {
          "access_token":token,
          "application_id":str(request.headers['application']),
          "organization_id":str(request.headers['organization']),
        }
        data = await rabbitmq.publish(
          payload=json.dumps(jsonable_encoder(payload)).encode(),
          exchange_name="gdmp-authorization",
          exchange_type=ExchangeType.DIRECT,
          routing_key="verify_access_token",
          callback_queue_name="verify_access_token_callback_queue",
          rpc=True          
        )
        rabbitmq_data = data

        if rabbitmq_data.get("success")==False:
          error_type = rabbitmq_data.get("error_type")
          error_message = rabbitmq_data.get("error_message")
          status_code = convert_error_type(error_type) if type(convert_error_type(error_type)) == int else 500
          return create_response(status_code=status_code, success=False, message=error_message)
          
        r_client.set(data.get('access_token'), json.dumps(data))
        r_client.expire(data.get('access_token'), REDIS_EXPIRE_MINUTES*60)
        user_data = r_client.get(token)
        if not user_data:
          return create_response(status_code=401, success=False, message="Token is invalid or has expired")

      user_data = json.loads(user_data)
      request.state.user = user_data.get("user")
      request.state.role = user_data.get("role")
      request.state.organization = user_data.get("current_organization")
      request.state.organizations = user_data.get("organizations",[])
      request.state.application = request.headers['application']

      return await call_next(request)
    elif "authorization" in request.headers:
      return create_response(status_code=401, success=False, message="Unauthorization header")
    else:
      return create_response(status_code=500, success=False, message="Authorization header not found")
