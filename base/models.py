from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from enum import Enum


class GenderEnum(str, Enum):
  MALE = "MALE"
  FEMALE = "FEMALE"
  OTHER = "OTHER"


class AbstractModel(BaseModel):
  id: UUID = Field(default_factory=uuid4)
  is_active: bool = True
  created_at: datetime = Field(default=None)
  updated_at: datetime = Field(default=None)
  
  @model_validator(mode = "before")
  @classmethod
  def set_default_values(cls, values):
    created_at = values.get("created_at")
    updated_at = values.get("updated_at")
    now = datetime.utcnow()
    if created_at is None:
      values["created_at"] = now
    if updated_at is None:
      values["updated_at"] = now
    return values
