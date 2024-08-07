from typing import Optional
from uuid import UUID
from pydantic import BaseModel, field_validator
from .models import TemplateTypeEnum
from .requirement.models import Requirement


class CreateTemplate(BaseModel):
  name: str
  categories: list[str]

  @field_validator("categories")
  @classmethod
  def validate_categories(cls, value):
    if len(value) == 0:
      raise ValueError("At least one category is required")
    return value


class ResponseTemplate(BaseModel):
  id: UUID
  name: str
  organization: UUID
  template_type: str
  categories: list[str]
  requirements: Optional[dict[str, dict[str, list[Requirement]]]] = None
  is_active: bool


class TemplateResponse(BaseModel):
  id:UUID
  name: str
  organization: UUID
  template_type: TemplateTypeEnum


class UpdateTemplateName(BaseModel):
  name: Optional[str] = None
