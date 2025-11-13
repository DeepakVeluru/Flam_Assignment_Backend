"""
Enqueue command - add jobs to the queue
"""

import click
import json
from src.core.models import Job
from src.storage.job_store import job_store


@click.command('enqueue')
@click.argument('job_json', required=False)
@click.option('--command', '-c', help='Command to execute')
@click.option('--max-retries', '-r', type=int, default=None, help='Max retries for this job')
def enqueue(job_json, command, max_retries):
    """
    Enqueue a new job
    
    Examples:
        queuectl enqueue '{"id":"job1","command":"echo hello"}'
        queuectl enqueue --command "sleep 2"
    """
    try:
        if job_json:
            # Parse JSON job
            job_data = json.loads(job_json)
            job = Job.from_dict(job_data)
        elif command:
            # Create job from command option
            job = Job(command=command)
            if max_retries is not None:
                job.max_retries = max_retries
        else:
            raise click.BadParameter("Either provide job JSON as argument or use --command")

        # Store the job
        job = job_store.add_job(job)

        click.echo(f"✓ Job enqueued: {job.id}")
        click.echo(f"  Command: {job.command}")
        click.echo(f"  State: {job.state.value}")
        click.echo(f"  Max retries: {job.max_retries}")

    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON: {e}")
    except Exception as e:
        raise click.ClickException(str(e))
