from __future__ import annotations

import json

from sqlalchemy.orm import Session

from app.core.worker import process_job
from app.db.models import Job


def test_process_word_count_job() -> None:
    job = Job(
        job_type="word_count",
        payload_json=json.dumps({"text": "hello world from john"}),
    )

    result = process_job(job)

    assert result == {"word_count": 4}


def test_process_uppercase_job() -> None:
    job = Job(
        job_type="uppercase",
        payload_json=json.dumps({"text": "hello"}),
    )

    result = process_job(job)

    assert result == {"result": "HELLO"}


def test_process_reverse_job() -> None:
    job = Job(
        job_type="reverse",
        payload_json=json.dumps({"text": "abc"}),
    )

    result = process_job(job)

    assert result == {"result": "cba"}


def test_process_unknown_job_type_raises_error() -> None:
    job = Job(
        job_type="unknown",
        payload_json=json.dumps({}),
    )

    try:
        process_job(job)
    except ValueError as exc:
        assert "Unsupported job_type" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
