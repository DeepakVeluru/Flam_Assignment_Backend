"""
Worker command - manage worker processes
"""

import click
import time
import signal
import sys
from src.worker.pool import worker_pool
from src.core.config import config


@click.group('worker')
def worker():
    """Manage worker processes"""
    pass


@worker.command('start')
@click.option('--count', '-c', type=int, default=1, help='Number of workers to start')
@click.option('--max-retries', '-r', type=int, default=None, help='Max retries for jobs')
def worker_start(count, max_retries):
    """Start one or more workers"""
    try:
        if count < 1:
            raise click.BadParameter("Count must be at least 1")

        if count > config.get('max_workers', 10):
            raise click.BadParameter(f"Count cannot exceed {config.get('max_workers', 10)}")

        if worker_pool.is_running():
            raise click.ClickException("Workers are already running. Stop them first with 'queuectl worker stop'")

        max_retries_val = max_retries or config.get('max_retries', 3)
        started = worker_pool.start_workers(count, max_retries_val)

        click.echo(f"✓ Started {started} worker(s)")
        click.echo(f"  Max retries per job: {max_retries_val}")
        click.echo(f"  Backoff base: {config.get('backoff_base', 2)}")
        click.echo("")
        click.echo("Workers are processing jobs. Press Ctrl+C to stop gracefully.")

        # Keep the process alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            click.echo("\nShutting down workers gracefully...")
            worker_pool.stop_workers()
            click.echo("✓ Workers stopped")

    except Exception as e:
        raise click.ClickException(str(e))


@worker.command('stop')
def worker_stop():
    """Stop running workers gracefully"""
    try:
        if not worker_pool.is_running():
            click.echo("No workers are running")
            return

        click.echo("Stopping workers gracefully...")
        worker_pool.stop_workers()
        click.echo("✓ Workers stopped")

    except Exception as e:
        raise click.ClickException(str(e))


@worker.command('info')
def worker_info():
    """Show information about running workers"""
    try:
        if not worker_pool.is_running():
            click.echo("No workers are running")
            return

        info = worker_pool.get_worker_info()
        click.echo(f"Workers: {info['active']}/{info['total']} active")

        for w in info['workers']:
            status = "✓ Running" if w['running'] else "✗ Stopped"
            job_info = f" (Job: {w['current_job']})" if w['current_job'] else ""
            click.echo(f"  Worker {w['id']}: {status}{job_info}")

    except Exception as e:
        raise click.ClickException(str(e))
