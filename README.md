# QueueCTL

A small, local CLI-based background job queue implemented in Python. QueueCTL lets you enqueue shell commands as jobs, run multiple workers to process them, and manage retries and a dead-letter queue (DLQ).

This repository contains a compact, easy-to-run queue designed for development and small workloads. It uses JSON files for storage and a thread-based worker pool.

## Features

- Enqueue shell commands as jobs
- Multiple workers (concurrent processing)
- Configurable retry count with exponential backoff
- Dead Letter Queue for permanently failed jobs
- Simple JSON-based persistence (no DB required)
- Helpful CLI built with Click

## Requirements

- Python 3.8+
- Install required packages:

```powershell
pip install -r requirements.txt
```

## Quick Start

1. From the project root, install dependencies (see above).
2. Enqueue a job:

```powershell
python queuectl.py enqueue --command "echo Hello from QueueCTL"
```

3. Start a worker to process jobs:

```powershell
python queuectl.py worker start --count 1
```

4. Check queue and worker status:

```powershell
python queuectl.py status
python queuectl.py list --state completed
```

5. Stop workers when done:

```powershell
python queuectl.py worker stop
```

For a scripted demo, run:

```powershell
python run_demo.py
```

## Common Commands

- Enqueue a job:
  - `python queuectl.py enqueue --command "sleep 1 && echo Job"`
  - `python queuectl.py enqueue --command "exit 1" --max-retries 2`
- Start/stop workers:
  - `python queuectl.py worker start --count 2`
  - `python queuectl.py worker stop`
- Inspect jobs:
  - `python queuectl.py list --state pending`
  - `python queuectl.py list --state failed --format json`
- DLQ management:
  - `python queuectl.py dlq list`
  - `python queuectl.py dlq retry <job-id>`

Use `python queuectl.py <command> --help` for per-command options and examples.

## Configuration

Default configuration is stored under the user home directory (e.g. `%USERPROFILE%\\.queuectl\\config.json` on Windows). You can inspect or change config via the CLI:

```powershell
python queuectl.py config show
python queuectl.py config set max-retries 5
```

## Tests

Run the test suite (if you have pytest installed):

```powershell
python -m pytest -q
```

## Project Layout

```
queuectl/
├── queuectl.py        # CLI entry point
├── run_demo.py        # Small demo script that exercises the CLI
├── requirements.txt   # Python deps
├── src/               # Application package (cli, core, storage, worker)
└── tests/             # Tests (unit & flow)
```

## Notes & Limitations

- Storage is file-based and best-suited for development or small deployments.
- This project is not a distributed queue; all workers run on the same host.
- For production-scale workloads, consider a DB-backed queue or a mature system (e.g. Celery, RQ).
## drive link:
https://drive.google.com/file/d/1NEeYenFGaEhi6kYGDJ7s8vMOGJfw13ZU/view?usp=drive_link

## License
MIT

---

If you want this README expanded with more examples, architecture diagrams, or contribution guidelines, tell me which sections to add and I will update it.
