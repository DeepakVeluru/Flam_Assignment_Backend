"""
File-based storage for jobs
"""

import json
import threading
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from src.core.models import Job, JobState
from src.core.config import config


class JobStore:
    """Thread-safe job storage"""

    def __init__(self):
        self.lock = threading.RLock()
        self.jobs_file = config.jobs_file
        self.dlq_file = config.dlq_file
        self._ensure_files()

    def _ensure_files(self):
        """Ensure storage files exist"""
        if not self.jobs_file.exists():
            with open(self.jobs_file, 'w') as f:
                json.dump([], f)

        if not self.dlq_file.exists():
            with open(self.dlq_file, 'w') as f:
                json.dump([], f)

    def add_job(self, job: Job) -> Job:
        """Add a new job"""
        with self.lock:
            jobs = self._read_jobs_file()
            jobs.append(job.to_dict())
            self._write_jobs_file(jobs)
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        """Get a job by ID"""
        with self.lock:
            jobs = self._read_jobs_file()
            for job_data in jobs:
                if job_data['id'] == job_id:
                    return Job.from_dict(job_data)
        return None

    def list_jobs(self, state: Optional[JobState] = None) -> List[Job]:
        """List all jobs, optionally filtered by state"""
        with self.lock:
            jobs = self._read_jobs_file()
            result = []
            for job_data in jobs:
                job = Job.from_dict(job_data)
                if state is None or job.state == state:
                    result.append(job)
            return result

    def update_job(self, job: Job) -> bool:
        """Update an existing job"""
        with self.lock:
            jobs = self._read_jobs_file()
            for i, job_data in enumerate(jobs):
                if job_data['id'] == job.id:
                    jobs[i] = job.to_dict()
                    self._write_jobs_file(jobs)
                    return True
        return False

    def delete_job(self, job_id: str) -> bool:
        """Delete a job"""
        with self.lock:
            jobs = self._read_jobs_file()
            jobs = [j for j in jobs if j['id'] != job_id]
            self._write_jobs_file(jobs)
            return True

    def move_to_dlq(self, job: Job) -> bool:
        """Move a job to DLQ"""
        with self.lock:
            # Add to DLQ
            dlq_jobs = self._read_dlq_file()
            job.state = JobState.DEAD
            job.updated_at = datetime.utcnow()
            dlq_jobs.append(job.to_dict())
            self._write_dlq_file(dlq_jobs)

            # Remove from main queue
            self.delete_job(job.id)
            return True

    def get_dlq_job(self, job_id: str) -> Optional[Job]:
        """Get a job from DLQ"""
        with self.lock:
            dlq_jobs = self._read_dlq_file()
            for job_data in dlq_jobs:
                if job_data['id'] == job_id:
                    return Job.from_dict(job_data)
        return None

    def list_dlq(self) -> List[Job]:
        """List all jobs in DLQ"""
        with self.lock:
            dlq_jobs = self._read_dlq_file()
            return [Job.from_dict(j) for j in dlq_jobs]

    def remove_from_dlq(self, job_id: str) -> bool:
        """Remove a job from DLQ"""
        with self.lock:
            dlq_jobs = self._read_dlq_file()
            dlq_jobs = [j for j in dlq_jobs if j['id'] != job_id]
            self._write_dlq_file(dlq_jobs)
            return True

    def retry_dlq_job(self, job_id: str) -> Optional[Job]:
        """Retry a DLQ job - move back to queue"""
        with self.lock:
            job = self.get_dlq_job(job_id)
            if not job:
                return None

            self.remove_from_dlq(job_id)
            job.state = JobState.PENDING
            job.attempts = 0
            job.updated_at = datetime.utcnow()
            self.add_job(job)
            return job

    def get_next_pending_job(self) -> Optional[Job]:
        """Get the next pending job (FIFO)"""
        with self.lock:
            jobs = self._read_jobs_file()
            now = datetime.utcnow()
            for job_data in jobs:
                job = Job.from_dict(job_data)
                if job.state == JobState.PENDING:
                    # Check if job is ready to retry
                    if job.next_retry_at is None or job.next_retry_at <= now:
                        return job
        return None

    def count_by_state(self) -> Dict[str, int]:
        """Count jobs by state"""
        with self.lock:
            jobs = self._read_jobs_file()
            counts = {state.value: 0 for state in JobState}
            for job_data in jobs:
                state = job_data.get('state', 'pending')
                if state in counts:
                    counts[state] += 1
            counts['dlq'] = len(self._read_dlq_file())
            return counts

    def _read_jobs_file(self) -> List[Dict]:
        """Read jobs from file (not thread-safe, call with lock)"""
        try:
            with open(self.jobs_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []

    def _write_jobs_file(self, jobs: List[Dict]):
        """Write jobs to file (not thread-safe, call with lock)"""
        with open(self.jobs_file, 'w') as f:
            json.dump(jobs, f, indent=2)

    def _read_dlq_file(self) -> List[Dict]:
        """Read DLQ jobs from file (not thread-safe, call with lock)"""
        try:
            with open(self.dlq_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []

    def _write_dlq_file(self, jobs: List[Dict]):
        """Write DLQ jobs to file (not thread-safe, call with lock)"""
        with open(self.dlq_file, 'w') as f:
            json.dump(jobs, f, indent=2)


# Global store instance
job_store = JobStore()
