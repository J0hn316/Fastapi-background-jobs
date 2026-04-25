from __future__ import annotations

import json

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db.models import Job
from app.schemas.jobs_schema import JobCreate


def create_job(db: Session, data: JobCreate) -> Job:
    job = Job(
        job_type=data.job_type,
        payload_json=json.dumps(data.payload, ensure_ascii=False),
        status="pending",
        attempt_count=0,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_job(db: Session, job_id: int) -> Job | None:
    return db.get(Job, job_id)


def list_jobs(
    db: Session,
    *,
    limit: int,
    offset: int,
    status: str | None = None,
    job_type: str | None = None,
) -> tuple[list[Job], int]:
    stmt: Select = select(Job)

    if status:
        stmt = stmt.where(Job.status == status)
    if job_type:
        stmt = stmt.where(Job.job_type == job_type)

    total_stmt = select(func.count()).select_from(stmt.subquery())

    stmt = stmt.order_by(Job.created_at.desc()).limit(limit).offset(offset)

    items = list(db.execute(stmt).scalars().all())
    total = int(db.execute(total_stmt).scalar_one())
    return items, total


def retry_job(db: Session, job: Job) -> Job:
    if job.status != "failed":
        raise ValueError("Only failed jobs can be retried")

    job.status = "pending"
    job.error_message = None
    job.result_json = None
    job.started_at = None
    job.finished_at = None

    db.commit()
    db.refresh(job)
    return job
