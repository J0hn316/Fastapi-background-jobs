# FastAPI Background Jobs

A FastAPI backend project for learning background job processing, worker loops, job lifecycle management, and API-driven task execution.

## Features

- Create background jobs through an API
- Store job state in SQLite
- Process jobs with a separate worker process
- Track job lifecycle:
  - pending
  - running
  - completed
  - failed
- Store job results and errors
- Retry failed jobs
- Filter jobs by status and job type
- Test API and worker logic with Pytest

## Tech Stack

- FastAPI
- SQLite
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- Pytest
- HTTPX

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python run.py
```

## Run Worker

- Open a second terminal

```bash
python worker.py
```
