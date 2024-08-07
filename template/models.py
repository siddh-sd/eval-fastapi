from enum import Enum
from uuid import UUID
from beanie import Document
from pymongo import ASCENDING, IndexModel
from base.models import AbstractModel


class TemplateTypeEnum(str, Enum):
  REQUIREMENTS_DB = "REQUIREMENTS_DB"
  GENERIC = "GENERIC"


class Template(AbstractModel, Document):
  name: str
  organization: UUID
  template_type: TemplateTypeEnum = TemplateTypeEnum.GENERIC
  categories: list[str]
    
  class Settings:
    name = 'templates'
    indexes = [
      IndexModel([("name", ASCENDING), ("organization", ASCENDING),("is_active", ASCENDING)], 
                 unique=True, name="name_organization_unique_index")
    ]