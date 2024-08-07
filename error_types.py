# from utils.exceptions import BadRequestError, EntityNotFoundError,UnauthorizedError
from base_utils.exception import BadRequestError, EntityNotFoundError,UnauthorizedError

def convert_error_type(error_type: str):
  exception_mapping = {
    "ExpiredSignatureError": 401,
    "InvalidTokenError": 401,
    "BadRequestError": BadRequestError,
    "EntityNotFoundError":EntityNotFoundError,
    "UnauthorizedError":UnauthorizedError,
  }
  error_type = exception_mapping.get(error_type,Exception)
  return error_type
