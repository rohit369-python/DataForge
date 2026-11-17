from pydantic import BaseModel, Field
from typing import Literal
class SourceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    source_type: Literal["csv", "excel", "json", "rest", "postgres", "mongodb", "kafka", "s3"] = "csv"
    description: str = ""
class PipelineCreate(BaseModel):
    name: str = Field(min_length=2, max_length=140)
    description: str = ""
    source_id: int | None = None
    schedule: str = "manual"
class PipelineUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    active: bool | None = None
    schedule: str | None = None
