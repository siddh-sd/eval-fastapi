from enum import Enum
from functools import wraps
from uuid import UUID

from fastapi import Request

from user_role.models import UserRole
from base_utils.utils import create_response

"""
Update the initialisation script with the following permissions:
ADMIN: { organization: 15, template: 15, evaluation: 15 }
EDITOR: { organization: 0, template: 15, evaluation: 15 }
"""

class Module(Enum):
  ORGANIZATION = "organization"
  TEMPLATE = "template"
  EVALUATION = "evaluation"
  MEMBER = "member"


class SubModule(Enum):
  ORGANIZATION = "organization"
  TEMPLATE = "template"
  EVALUATION = "evaluation"
  EVALUATION_TEMPLATE = "evaluation_template"
  EVALUATION_DOC = "evaluation_doc"
  EVALUATION_CATEGORY = "category"
  REQUIREMENT = "requirement"
  MEMBER = "member"


class Permission(Enum):
  CREATE = 1
  READ = 2
  UPDATE = 4
  DELETE = 8


def check_permission(value: int, permission: Permission) -> bool:
  return value % (permission.value * 2) >= permission.value


def has_access(permission: Permission, module: Module, sub_module: SubModule):
  def decorator(func):
    @wraps(func)
    async def wrapper(request: Request, id: UUID = None, *args, **kwargs):
      try:
        if module == Module.MEMBER and (request.state.role.get("name") in ["ADMIN","EDITOR"] ):
          role = request.state.role
        else:
          if id is not None:
            criteria = { f'{module.value}.id': id }
            user_role = await UserRole.find(
              UserRole.user.id == UUID(request.state.user["id"]),
              UserRole.organization.id == UUID(request.state.organization["id"]),
            ).find(criteria).to_list()
            
            if len(user_role) == 0:
              return create_response(status_code=403, success=False, message="You don't have access to this resource")
            role = user_role[0].role.model_dump()
          else:
            role = request.state.role

        if not check_permission(role["permissions"][sub_module.value], permission):
          return create_response(status_code=403, success=False, message="You don't have access to this resource")
        
        if id is not None:
          return await func(request=request, id=id, *args, **kwargs)
        else:
          return await func(request=request, *args, **kwargs)

      except Exception as e:
        return create_response(status_code=500, success=False, message=str(e))
    return wrapper
  return decorator