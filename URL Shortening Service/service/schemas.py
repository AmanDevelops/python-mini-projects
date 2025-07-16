from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateUrl(BaseModel):
    url: str


class CreateUrlResponse(BaseModel):
    id: int
    message: str = "URL Created Succesfully"
    url: str
    short_code: str
    created_at: datetime
    updated_at: datetime
    created_by: int
    views: int


class UpdateUrl(BaseModel):
    id: int
    short_code: Optional[str] = None
    url: Optional[str] = None


class UpdateUrlResponse(BaseModel):
    id: int
    message: str = "URL Updated Succesfully"
    url: str
    short_code: str
    created_at: datetime
    updated_at: datetime
    created_by: str
