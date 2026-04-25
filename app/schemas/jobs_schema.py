from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    job_type: str = Field(min_length=1, max_length=100)
    payload: dict[str, Any]


class JobOut(BaseModel):
    id: int
    job_type: str
    payload_json: str
    status: str
    result_json: str | None
    error_message: str | None
    attempt_count: int
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None

    model_config = {"from_attributes": True}


class JobsListOut(BaseModel):
    items: list[JobOut]
    total: int
    limit: int
    offset: int
