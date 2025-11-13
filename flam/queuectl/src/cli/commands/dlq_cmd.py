"""
DLQ command - manage Dead Letter Queue
"""

import click
from tabulate import tabulate
from src.storage.job_store import job_store
from src.core.models import Job


@click.group('dlq')
def dlq():
    """Manage Dead Letter Queue"""
    pass


@dlq.command('list')
@click.option('--format', '-f', type=click.Choice(['table', 'json']), default='table', help='Output format')
def dlq_list(format):
    """List jobs in the Dead Letter Queue"""
    try:
        jobs = job_store.list_dlq()

        if not jobs:
            click.echo("Dead Letter Queue is empty")
            return

        if format == 'json':
            import json
            click.echo(json.dumps([j.to_dict() for j in jobs], indent=2, default=str))
        else:
            # Table format
            table_data = []
            for job in jobs:
                table_data.append([
                    job.id[:8],
                    job.command[:40] + '...' if len(job.command) > 40 else job.command,
                    job.attempts,
                    job.max_retries,
                    job.error[:50] + '...' if job.error and len(job.error) > 50 else (job.error or '-')
                ])

            click.echo(tabulate(
                table_data,
                headers=['ID', 'Command', 'Attempts', 'Max Retries', 'Error'],
                tablefmt='simple'
            ))

            click.echo(f"\nTotal in DLQ: {len(jobs)}")

    except Exception as e:
        raise click.ClickException(str(e))


@dlq.command('retry')
@click.argument('job_id')
def dlq_retry(job_id):
    """Retry a job from the Dead Letter Queue"""
    try:
        job = job_store.retry_dlq_job(job_id)

        if not job:
            raise click.ClickException(f"Job {job_id} not found in DLQ")

        click.echo(f"✓ Job {job.id} moved back to queue")
        click.echo(f"  Command: {job.command}")
        click.echo(f"  State: {job.state.value}")
        click.echo(f"  Attempts reset to: {job.attempts}")

    except click.ClickException:
        raise
    except Exception as e:
        raise click.ClickException(str(e))


@dlq.command('remove')
@click.argument('job_id')
def dlq_remove(job_id):
    """Remove a job from the Dead Letter Queue permanently"""
    try:
        if job_store.remove_from_dlq(job_id):
            click.echo(f"✓ Job {job_id} removed from DLQ")
        else:
            raise click.ClickException(f"Job {job_id} not found in DLQ")

    except click.ClickException:
        raise
    except Exception as e:
        raise click.ClickException(str(e))


@dlq.command('details')
@click.argument('job_id')
def dlq_details(job_id):
    """Show detailed information about a DLQ job"""
    try:
        job = job_store.get_dlq_job(job_id)

        if not job:
            raise click.ClickException(f"Job {job_id} not found in DLQ")

        click.echo("=" * 60)
        click.echo(f"Job Details: {job.id}")
        click.echo("=" * 60)
        click.echo(f"Command: {job.command}")
        click.echo(f"State: {job.state.value}")
        click.echo(f"Attempts: {job.attempts}/{job.max_retries}")
        click.echo(f"Created: {job.created_at}")
        click.echo(f"Updated: {job.updated_at}")

        if job.error:
            click.echo(f"\nError:")
            click.echo(f"  {job.error}")

        if job.output:
            click.echo(f"\nOutput:")
            click.echo(f"  {job.output[:500]}")
            if len(job.output) > 500:
                click.echo("  (truncated)")

    except click.ClickException:
        raise
    except Exception as e:
        raise click.ClickException(str(e))
