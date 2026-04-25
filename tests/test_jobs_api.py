from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_job_success(client: TestClient) -> None:
    response = client.post(
        "/jobs",
        json={
            "job_type": "word_count",
            "payload": {"text": "hello world from john"},
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["job_type"] == "word_count"
    assert data["status"] == "pending"
    assert data["attempt_count"] == 0
    assert "id" in data


def test_list_jobs_returns_created_job(client: TestClient) -> None:
    client.post(
        "/jobs",
        json={
            "job_type": "uppercase",
            "payload": {"text": "hello"},
        },
    )

    response = client.get("/jobs")

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1


def test_get_job_success(client: TestClient) -> None:
    create_response = client.post(
        "/jobs",
        json={
            "job_type": "reverse",
            "payload": {"text": "abc"},
        },
    )

    job_id = create_response.json()["id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json()["id"] == job_id


def test_retry_non_failed_job_returns_400(client: TestClient) -> None:
    create_response = client.post(
        "/jobs",
        json={
            "job_type": "word_count",
            "payload": {"text": "hello"},
        },
    )

    job_id = create_response.json()["id"]

    response = client.post(f"/jobs/{job_id}/retry")

    assert response.status_code == 400
    assert response.json()["detail"] == "Only failed jobs can be retried"


def test_get_missing_job_returns_404(client: TestClient) -> None:
    response = client.get("/jobs/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"
