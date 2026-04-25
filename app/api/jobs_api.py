from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.jobs_schema import JobCreate, JobOut, JobsListOut
from app.services.jobs_service import create_job, get_job, list_jobs, retry_job

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


@router.post("", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job_route(payload: JobCreate, db: Session = Depends(get_db)) -> JobOut:
    job = create_job(db, payload)
    return job


@router.get("", response_model=JobsListOut)
def list_jobs_route(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: str | None = Query(default=None),
    job_type: str | None = Query(default=None),
) -> JobsListOut:
    items, total = list_jobs(
        db,
        limit=limit,
        offset=offset,
        status=status,
        job_type=job_type,
    )
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{job_id}", response_model=JobOut)
def get_job_route(job_id: int, db: Session = Depends(get_db)) -> JobOut:
    job = get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/{job_id}/retry", response_model=JobOut)
def retry_job_route(job_id: int, db: Session = Depends(get_db)) -> JobOut:
    job = get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    try:
        job = retry_job(db, job)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return job
