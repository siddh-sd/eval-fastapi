import asyncio
import csv
from io import StringIO
from typing import Annotated
from uuid import UUID, uuid4
import beanie
from fastapi import APIRouter, Form, Request, UploadFile
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from user_role.models import UserRole
from user_role.service import UserRoleService
from utils import Details
from base_utils.exception import EntityNotFoundError, UnauthorizedError
from base_utils.utils import create_response, create_updated_fields
from .dtos import (CreateTemplate, ResponseTemplate,
                   TemplateResponse, UpdateTemplateName)
from .models import Template
from .requirement.models import Requirement, RequirementView, RequirementCategoryTopicView
from .requirement.routes import router as requirement_router
from middleware.service import has_access, Module, SubModule, Permission
import sentry_sdk
from base.utils import obj_to_model_dump

router = APIRouter(tags=["Template"])

router.include_router(requirement_router, prefix="/requirement", tags=["Requirement"])



@router.post('', status_code=201)
@has_access(Permission.CREATE, Module.TEMPLATE, SubModule.TEMPLATE)
async def create(request: Request, request_body: CreateTemplate):
  """
  Creates a new template with the provided details, ensuring unique template names within the organization.
  """
  try:
    template = Template(
      name=request_body.name, 
      organization=UUID(request.state.organization["id"]),
      categories = request_body.categories
    )
    await template.save()

    user_role = await UserRoleService.create_user_role_template(
      user=request.state.user, 
			organization=request.state.organization, 
			role=request.state.role,
      template=Details(id=template.id, name=template.name),
      save=False
    )
    await user_role.save()
      
    return create_response(
      status_code=201,
      success=True, 
      message='Templates has been created successfully', 
      data=ResponseTemplate(**obj_to_model_dump(template), requirements={})
    )
  
  except DuplicateKeyError as dke:
    sentry_sdk.capture_exception(dke)
    return create_response(status_code=409, message="Duplicate Template Name Error")
    
  except UnauthorizedError as ue:
    sentry_sdk.capture_exception(ue)
    return create_response(status_code=ue.status_code, message=str(ue))
  
  except EntityNotFoundError as enfe:
    sentry_sdk.capture_exception(enfe)
    return create_response(status_code=enfe.status_code, message=str(enfe))

  except beanie.exceptions.RevisionIdWasChanged as dke:
    return create_response(status_code=409, message="Template is already exist.")
  
  except Exception as e:
    sentry_sdk.capture_exception(e)
    return create_response(status_code=500, success=False, message=str(e))
