# Flam_Assignment_Backend


#  QueueCTL - Background Job Queue Management System

A **production-grade CLI-based job queue system** written in Python. Manage background jobs with multiple worker processes, automatic retry with exponential backoff, and a Dead Letter Queue for permanently failed jobs.

#### 2  **Python 3.8+** 
```bash
python --version
# Should show: Python 3.8 or higher
```

#### 3️ **Install Dependencies** 
```bash
pip install -r requirements.txt
```

**That's it! Nothing else is required.** 

---

## WHAT'S NOT REQUIRED

These files are **optional helpers** - system works fine without them:

| File | Type | Why Optional |
|------|------|-------------|
| `setup.ps1` | Setup script | Manual install works |
| `setup.sh` | Setup script | Manual install works |
| `queuectl.bat` | Windows wrapper | Use `python queuectl.py` |
| `RUN_FULL_DEMO.ps1` | Demo automation | Run commands manually |
| All demo scripts | Testing | Not required to run |
| Documentation files | Help docs | README.md is enough |

---

## Features

**Job Enqueuing** - Add jobs via CLI with custom commands  
**Multiple Workers** - Process jobs concurrently with configurable worker count  
**Exponential Backoff** - Automatic retry with configurable backoff strategy  
**Dead Letter Queue** - Track and manage permanently failed jobs  
**Persistent Storage** - Jobs survive application restarts using JSON files  
**Graceful Shutdown** - Workers finish current jobs before exiting  
**Configuration Management** - Customize retries, backoff, worker limits  
**Comprehensive CLI** - User-friendly commands with detailed help

---

## Installation

### Step 1: Install Dependencies (REQUIRED)
```bash
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
python queuectl.py --version
# Expected output: queuectl.py, version 1.0.0
```

### Step 3: Check Configuration
```bash
python queuectl.py config show
# Shows settings and storage paths
```

---

## Requirements

- **Python 3.8+**
- Dependencies: `click`, `pydantic`, `tabulate`, `python-dotenv`

---

## Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
cd queuectl
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
python queuectl.py --version
# Output: queuectl.py, version 1.0.0
```

### Step 3: Enqueue Jobs
```bash
python queuectl.py enqueue --command "echo Job 1"
python queuectl.py enqueue --command "echo Job 2"
python queuectl.py enqueue --command "echo Job 3"
```

### Step 4: Start Workers
```bash
python queuectl.py worker start --count 2
# Let run for 10 seconds, then Ctrl+C
```

### Step 5: Check Results
```bash
python queuectl.py status
python queuectl.py list --state completed
```

**Done! 3 jobs processed in parallel.** 

---

## Usage Guide

### Basic Commands

#### 1. **Enqueue Jobs**
Add a new job to the queue:

```bash
# Simple command
python queuectl.py enqueue --command "echo hello world"

# With max retries
python queuectl.py enqueue --command "python script.py" --max-retries 3
```

#### 2. **Start Workers**
Begin processing jobs:

```bash
# Start 1 worker
python queuectl.py worker start

# Start 3 workers
python queuectl.py worker start --count 3
```

#### 3. **Stop Workers**
```bash
python queuectl.py worker stop
```

#### 4. **Check Status**
```bash
python queuectl.py status
```

#### 5. **List Jobs**
```bash
python queuectl.py list
python queuectl.py list --state pending
python queuectl.py list --state completed
python queuectl.py list --state failed
python queuectl.py list --format json
```

#### 6. **Manage Dead Letter Queue**
```bash
python queuectl.py dlq list
python queuectl.py dlq retry <job-id>
python queuectl.py dlq remove <job-id>
```

#### 7. **Configuration**
```bash
python queuectl.py config show
python queuectl.py config set max-retries 10
python queuectl.py config get max-retries
python queuectl.py config reset
```

---

## Architecture

### Four-Layer Design

**Layer 1: CLI** (`queuectl.py`)  
→ Command-line interface with Click framework

**Layer 2: Core** (`src/core/`)  
→ Job models, configuration, execution logic

**Layer 3: Storage** (`src/storage/`)  
→ Thread-safe JSON persistence

**Layer 4: Workers** (`src/worker/`)  
→ Multi-threaded job processing

---

## Data Storage

```
~/.queuectl/
├── config.json          # Settings
├── workers.pid          # Active workers
└── data/
    ├── jobs.json        # Job queue
    └── dlq.json         # Dead Letter Queue
```

---

## Job States

- **PENDING** - Waiting for processing
- **PROCESSING** - Currently executing
- **COMPLETED** - Successfully finished
- **FAILED** - Failed, will retry
- **DEAD** - Permanently failed (DLQ)

---

## Requirements

- **Python 3.8+**
- Dependencies: `click`, `pydantic`, `tabulate`, `python-dotenv`

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd queuectl
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Make CLI Executable (Optional)
Create an alias or install as a script:

**On Linux/macOS:**
```bash
chmod +x queuectl.py
ln -s $(pwd)/queuectl.py /usr/local/bin/queuectl
```

**On Windows:**
Add this script to your PATH or use:
```powershell
python queuectl.py <command>
```

---

## Usage Guide

### Basic Commands

#### 1. **Enqueue Jobs**
Add a new job to the queue:

```bash
# Simple command
python queuectl.py enqueue --command "echo hello world"

# With JSON
python queuectl.py enqueue '{"id":"job1","command":"sleep 2","max_retries":5}'

# With max retries
python queuectl.py enqueue --command "python script.py" --max-retries 3
```

#### 2. **Start Workers**
Begin processing jobs:

```bash
# Start 1 worker
python queuectl.py worker start

# Start 3 workers
python queuectl.py worker start --count 3

# Start with custom max retries
python queuectl.py worker start --count 2 --max-retries 5
```

The process will continue until you press `Ctrl+C` (graceful shutdown).

#### 3. **Stop Workers**
Stop running workers gracefully:

```bash
python queuectl.py worker stop
```

#### 4. **Check Status**
View queue and worker status:

```bash
python queuectl.py status
```

**Output Example:**
```
==================================================
JOB QUEUE STATUS
==================================================
State                Count
-----------------  -------
Pending                  2
Processing               1
Completed                5
Failed                   0
Dead Letter Queue        1

Total Jobs: 9

==================================================
WORKER STATUS
==================================================
Active Workers: 2/3
  ✓ Worker 0 [Job: abc12345]
  ✓ Worker 1
  ✗ Worker 2
```

#### 5. **List Jobs**
View jobs filtered by state:

```bash
# List all jobs
python queuectl.py list

# List pending jobs
python queuectl.py list --state pending

# List failed jobs with JSON output
python queuectl.py list --state failed --format json

# Show only first 10 jobs
python queuectl.py list --limit 10
```

#### 6. **Dead Letter Queue (DLQ)**

```bash
# List all jobs in DLQ
python queuectl.py dlq list

# Show details of a job
python queuectl.py dlq details <job-id>

# Retry a job from DLQ (resets attempts to 0)
python queuectl.py dlq retry <job-id>

# Remove a job from DLQ permanently
python queuectl.py dlq remove <job-id>
```

#### 7. **Configuration Management**

```bash
# Set max retries to 5
python queuectl.py config set max-retries 5

# Set exponential backoff base to 3
python queuectl.py config set backoff-base 3

# View a specific config
python queuectl.py config get max-retries

# View all configuration
python queuectl.py config get

# Show all config and storage paths
python queuectl.py config show

# Reset to defaults
python queuectl.py config reset
```

---

## Job Lifecycle

| State | Description |
|-------|-------------|
| **pending** | Waiting to be picked up by a worker |
| **processing** | Currently being executed by a worker |
| **completed** | Successfully executed |
| **failed** | Failed, but retryable (waiting for retry) |
| **dead** | Permanently failed (in DLQ) |

### Retry & Backoff Logic

When a job fails:
1. `attempts` counter increments
2. If `attempts < max_retries`:
   - Job state → `failed`
   - Next retry scheduled at: `now + (backoff_base ^ attempts) seconds`
   - Example with `backoff_base=2`:
     - 1st retry: 2^1 = 2 seconds
     - 2nd retry: 2^2 = 4 seconds
     - 3rd retry: 2^3 = 8 seconds

3. If `attempts >= max_retries`:
   - Job moves to **Dead Letter Queue**
   - State → `dead`
   - Can be retried manually via `dlq retry` or removed

---

##  Configuration

Default configuration is stored in `~/.queuectl/config.json`:

```json
{
  "max_retries": 3,
  "backoff_base": 2,
  "max_workers": 10,
  "worker_timeout": 3600
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `max_retries` | 3 | Default maximum retry attempts per job |
| `backoff_base` | 2 | Base for exponential backoff calculation |
| `max_workers` | 10 | Maximum workers allowed to start |
| `worker_timeout` | 3600 | Timeout per job execution (seconds) |

### Modify Configuration

```bash
python queuectl.py config set max-retries 5
python queuectl.py config set backoff-base 3
python queuectl.py config set max-workers 20
```

---

## Data Storage

All data is stored in `~/.queuectl/`:

```
~/.queuectl/
├── config.json          # Configuration
├── workers.pid          # Active worker PIDs
└── data/
    ├── jobs.json        # Main job queue
    └── dlq.json         # Dead Letter Queue
```

---

## Testing & Validation

### Test Script Scenarios

Run the provided test script to validate all core functionality:

```bash
python tests/test_flows.py
```

### Manual Test Scenarios

#### Scenario 1: Successful Job
```bash
# Terminal 1: Start worker
python queuectl.py worker start --count 1

# Terminal 2: Add a simple job
python queuectl.py enqueue --command "echo 'Hello from QueueCTL'"

# Check status
python queuectl.py status
# Expected: Job in COMPLETED state
```

#### Scenario 2: Job with Failure & Retry
```bash
# Terminal 1: Start worker
python queuectl.py worker start --count 1

# Terminal 2: Add a failing job
python queuectl.py enqueue --command "exit 1" --max-retries 3

# Check status immediately
python queuectl.py list --state failed

# Wait and check again (job should be pending for retry)
sleep 5
python queuectl.py list --state pending
```

#### Scenario 3: Multiple Workers
```bash
# Terminal 1: Start 3 workers
python queuectl.py worker start --count 3

# Terminal 2: Enqueue multiple jobs
for i in {1..10}; do
  python queuectl.py enqueue --command "sleep 1 && echo Job $i"
done

# Check status
python queuectl.py status
# Expected: Jobs distributed across workers
```

#### Scenario 4: Persistence After Restart
```bash
# Terminal 1: Start worker
python queuectl.py worker start --count 1

# Terminal 2: Enqueue jobs
python queuectl.py enqueue --command "sleep 100" --max-retries 2

# In Terminal 1: Press Ctrl+C to stop workers

# Verify job is still there
python queuectl.py list --state processing

# Restart workers
python queuectl.py worker start --count 1
# Worker will resume the job
```

#### Scenario 5: Dead Letter Queue
```bash
# Enqueue a job that will fail
python queuectl.py enqueue --command "false" --max-retries 2

# Start worker
python queuectl.py worker start

# Wait for job to exhaust retries (observe with status)
python queuectl.py list --state dead

# View DLQ
python queuectl.py dlq list

# Retry the job
python queuectl.py dlq retry <job-id>

# Job is back in queue as PENDING
```

---

##  Architecture Overview

### Components

1. **CLI Layer** (`src/cli/commands/`)
   - Command handlers using Click framework
   - Argument parsing and validation
   - User-friendly error messages

2. **Core Layer** (`src/core/`)
   - `models.py`: Job model definition
   - `config.py`: Configuration management
   - `executor.py`: Job execution and retry logic

3. **Storage Layer** (`src/storage/`)
   - `job_store.py`: Thread-safe job persistence using JSON
   - Lock-based synchronization for concurrent access

4. **Worker Layer** (`src/worker/`)
   - `pool.py`: Worker thread management
   - Parallel job processing
   - Graceful shutdown handling

### Data Flow

```
Enqueue Job
    ↓
[PENDING] → Worker picks up
    ↓
[PROCESSING] → Execute command
    ├─ SUCCESS → [COMPLETED]
    └─ FAILURE → Check attempts
                  ├─ retries left → [FAILED] (schedule retry)
                  └─ no retries → [DEAD] (move to DLQ)
```

### Concurrency & Locking

- **Thread-safe job storage** with RLock (reentrant lock)
- **Worker pool** manages multiple threads
- **No duplicate processing** ensured by atomic state transitions

---

##  Configuration Options

### Via CLI
```bash
python queuectl.py config set max-retries 5
python queuectl.py config set backoff-base 3
```

### Via config.json
Edit `~/.queuectl/config.json`:
```json
{
  "max_retries": 5,
  "backoff_base": 3,
  "max_workers": 20,
  "worker_timeout": 7200
}
```

---

##  Troubleshooting

### Issue: "Workers already running"
**Solution:** Stop existing workers first
```bash
python queuectl.py worker stop
```

### Issue: Jobs not progressing
**Solution:** Check if workers are running
```bash
python queuectl.py status
python queuectl.py worker start --count 2
```

### Issue: Jobs stuck in PROCESSING
**Possible causes:**
- Worker crashed
- Command is hanging
- Timeout expired

**Solution:** Restart workers
```bash
python queuectl.py worker stop
python queuectl.py worker start --count 1
```

### Issue: View storage location
```bash
python queuectl.py config show
```

---

##  Example Use Cases

### 1. Email Sending Queue
```bash
python queuectl.py enqueue --command "python send_email.py user@example.com"
python queuectl.py worker start --count 3
```

### 2. Data Processing Pipeline
```bash
python queuectl.py enqueue --command "python process_data.py input.csv output.csv"
python queuectl.py status  # Monitor progress
```

### 3. Periodic Cleanup
```bash
python queuectl.py enqueue --command "rm /tmp/old_files/*"
python queuectl.py worker start --count 1 --max-retries 2
```

---

##  Bonus Features Implemented

 **Job timeout handling** - Configurable per-job timeout with graceful failures  
 **Detailed job output logging** - Capture stdout/stderr from executed commands  
 **Worker process info** - View which worker is processing which job  
 **Comprehensive status dashboard** - Real-time queue and worker statistics  

---

## Assumptions & Trade-offs

### Assumptions
1. **Single-machine deployment** - All workers run on same machine (no distributed setup)
2. **JSON file storage** - Suitable for small to medium workloads (<100k jobs)
3. **Shell command execution** - Commands run via shell (supports pipes, redirects)
4. **Graceful shutdown** - Assumes workers have time to finish before hard kill

### Trade-offs
1. **File-based storage** over database for simplicity and zero setup
2. **Thread-based workers** instead of processes for easier job state sharing
3. **No job priority queue** - FIFO ordering for simplicity
4. **Local paths** instead of S3/cloud storage

### Scalability Considerations
For production use with large job volumes:
- Migrate to SQLite or PostgreSQL for better concurrency
- Use process-based workers (multiprocessing) instead of threads
- Consider Celery or RQ for distributed processing
- Add job priority queues
- Implement metrics collection (Prometheus)

---

##  Project Structure

```
queuectl/
├── queuectl.py                  # Main CLI entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── src/
│   ├── cli/
│   │   └── commands/
│   │       ├── enqueue_cmd.py   # Enqueue command
│   │       ├── worker_cmd.py    # Worker management
│   │       ├── status_cmd.py    # Status display
│   │       ├── list_cmd.py      # List jobs
│   │       ├── dlq_cmd.py       # DLQ management
│   │       └── config_cmd.py    # Configuration
│   ├── core/
│   │   ├── models.py            # Job model
│   │   ├── config.py            # Configuration management
│   │   └── executor.py          # Job execution & retry logic
│   ├── storage/
│   │   └── job_store.py         # Persistent job storage
│   └── worker/
│       └── pool.py              # Worker pool & thread management
└── tests/
    ├── test_flows.py            # Integration test scenarios
    └── test_basic.py            # Unit tests
```

---

##  Quick Start Example

```bash
# 1. Install
pip install -r requirements.txt

# 2. Enqueue some jobs
python queuectl.py enqueue --command "echo 'Job 1'"
python queuectl.py enqueue --command "sleep 2 && echo 'Job 2'"
python queuectl.py enqueue --command "false"  # Will fail and retry

# 3. Start workers
python queuectl.py worker start --count 2

# 4. Monitor in another terminal
python queuectl.py status

# 5. View completed jobs
python queuectl.py list --state completed

# 6. Stop workers
python queuectl.py worker stop
```

---

## Support & Debugging

### Enable Verbose Output
Most commands support `--help`:
```bash
python queuectl.py enqueue --help
python queuectl.py worker start --help
python queuectl.py config set --help
```

### Check Configuration
```bash
python queuectl.py config show
```

### View Storage Files
```bash
# On Linux/macOS
ls -la ~/.queuectl/
cat ~/.queuectl/config.json
cat ~/.queuectl/data/jobs.json

# On Windows
dir %USERPROFILE%\.queuectl\
type %USERPROFILE%\.queuectl\config.json
```

---

## License

MIT License - Feel free to use in your projects

---

## Evaluation Checklist

- [x] Working CLI application (`queuectl`)
- [x] Persistent job storage (JSON files)
- [x] Multiple worker support with thread pooling
- [x] Retry mechanism with exponential backoff
- [x] Dead Letter Queue for failed jobs
- [x] Configuration management via CLI
- [x] Clean, modular code structure
- [x] Comprehensive README with examples
- [x] Test scenarios demonstrating all features
- [x] Graceful shutdown and error handling

---

**Created for Backend Developer Internship Assignment**  
For issues or improvements, please submit a GitHub issue or PR.
