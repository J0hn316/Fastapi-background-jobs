from __future__ import annotations

import json
import time
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Job
from app.db.session import SessionLocal


def process_job(job: Job) -> dict:
    payload = json.loads(job.payload_json)

    if job.job_type == "word_count":
        text = payload.get("text", "")
        return {"word_count": len(text.split())}

    elif job.job_type == "uppercase":
        text = payload.get("text", "")
        return {"result": text.upper()}

    elif job.job_type == "reverse":
        text = payload.get("text", "")
        return {"result": text[::-1]}

    else:
        raise ValueError(f"Unsupported job_type: {job.job_type}")


def worker_loop() -> None:
    print("🚀 Worker started...")

    while True:
        db: Session = SessionLocal()

        try:
            stmt = (
                select(Job)
                .where(Job.status == "pending")
                .order_by(Job.created_at.asc())
                .limit(1)
            )

            job = db.execute(stmt).scalar_one_or_none()

            if job is None:
                time.sleep(settings.worker_poll_interval_seconds)
                continue

            # Claim job
            job.status = "running"
            job.started_at = datetime.now(UTC)
            job.attempt_count += 1
            db.commit()
            db.refresh(job)

            print(f"🔧 Processing job {job.id} ({job.job_type})")

            try:
                result = process_job(job)

                job.status = "completed"
                job.result_json = json.dumps(result, ensure_ascii=False)
                job.finished_at = datetime.now(UTC)

                print(f"✅ Job {job.id} completed")

            except Exception as exc:
                job.status = "Failed"
                job.error_message = str(exc)
                job.finished_at - datetime.now(UTC)

                print(f"❌ Job {job.id} failed: {exc}")

            db.commit()
        finally:
            db.close()
