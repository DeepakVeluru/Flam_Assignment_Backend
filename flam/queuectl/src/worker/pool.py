"""
Worker process implementation
"""

import threading
import signal
import time
import sys
from datetime import datetime
from pathlib import Path
import json
import os

from src.core.models import Job, JobState
from src.core.executor import JobExecutor
from src.storage.job_store import job_store
from src.core.config import config


class Worker(threading.Thread):
    """Worker thread that processes jobs"""

    def __init__(self, worker_id: int, max_retries: int = None):
        super().__init__(daemon=False)
        self.worker_id = worker_id
        self.executor = JobExecutor()
        self.max_retries = max_retries or config.get('max_retries', 3)
        self.running = True
        self.current_job = None
        self._lock = threading.Lock()

    def run(self):
        """Main worker loop"""
        try:
            while self.running:
                job = job_store.get_next_pending_job()

                if job is None:
                    time.sleep(0.5)  # Sleep briefly before checking again
                    continue

                # Mark as processing
                with self._lock:
                    self.current_job = job
                    job.state = JobState.PROCESSING
                    job.updated_at = datetime.utcnow()
                    job_store.update_job(job)

                try:
                    # Execute the job
                    success, output, error = self.executor.execute(job)

                    job.output = output
                    job.error = error
                    job.updated_at = datetime.utcnow()

                    if success:
                        # Job succeeded
                        job.state = JobState.COMPLETED
                        job_store.update_job(job)
                    else:
                        # Job failed
                        job.attempts += 1

                        if job.attempts >= self.max_retries:
                            # Move to DLQ
                            job.state = JobState.DEAD
                            job_store.move_to_dlq(job)
                        else:
                            # Schedule retry
                            job.state = JobState.FAILED
                            job.next_retry_at = self.executor.calculate_backoff(job)
                            job_store.update_job(job)

                except Exception as e:
                    job.error = str(e)
                    job.attempts += 1
                    job.updated_at = datetime.utcnow()

                    if job.attempts >= self.max_retries:
                        job.state = JobState.DEAD
                        job_store.move_to_dlq(job)
                    else:
                        job.state = JobState.FAILED
                        job.next_retry_at = self.executor.calculate_backoff(job)
                        job_store.update_job(job)

                finally:
                    with self._lock:
                        self.current_job = None

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the worker gracefully"""
        self.running = False
        # Wait for current job to finish
        while self.current_job is not None:
            time.sleep(0.1)

    def is_running(self) -> bool:
        """Check if worker is running"""
        return self.running and self.is_alive()


class WorkerPool:
    """Manages multiple worker threads"""

    def __init__(self):
        self.workers = []
        self._lock = threading.Lock()
        self.pid_file = config.pid_file

    def start_workers(self, count: int, max_retries: int = None):
        """Start multiple workers"""
        with self._lock:
            if len(self.workers) > 0:
                raise RuntimeError("Workers already running. Stop them first.")

            for i in range(count):
                worker = Worker(i, max_retries)
                worker.start()
                self.workers.append(worker)

            # Save PIDs
            self._save_pids()

            return len(self.workers)

    def stop_workers(self):
        """Stop all workers gracefully"""
        with self._lock:
            for worker in self.workers:
                worker.stop()

            # Wait for all workers to finish
            for worker in self.workers:
                worker.join(timeout=10)

            self.workers = []
            self._clean_pids()

    def get_active_workers(self) -> int:
        """Get count of active workers"""
        with self._lock:
            return len([w for w in self.workers if w.is_running()])

    def _save_pids(self):
        """Save worker PIDs to file"""
        pids = [os.getpid()]  # Current process PID
        with open(self.pid_file, 'w') as f:
            json.dump({'pids': pids, 'count': len(self.workers)}, f)

    def _clean_pids(self):
        """Clean up PID file"""
        if self.pid_file.exists():
            self.pid_file.unlink()

    def is_running(self) -> bool:
        """Check if any workers are running"""
        return len(self.workers) > 0

    def get_worker_info(self) -> dict:
        """Get information about running workers"""
        with self._lock:
            active = len([w for w in self.workers if w.is_running()])
            return {
                'total': len(self.workers),
                'active': active,
                'workers': [
                    {
                        'id': w.worker_id,
                        'running': w.is_running(),
                        'current_job': w.current_job.id if w.current_job else None
                    }
                    for w in self.workers
                ]
            }


# Global worker pool
worker_pool = WorkerPool()
