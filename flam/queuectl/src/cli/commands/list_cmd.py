"""
List command - list jobs by state
"""

import click
from tabulate import tabulate
from src.storage.job_store import job_store
from src.core.models import JobState


@click.command('list')
@click.option('--state', '-s', type=click.Choice(['pending', 'processing', 'completed', 'failed']), 
              default=None, help='Filter by job state')
@click.option('--limit', '-l', type=int, default=20, help='Limit number of results')
@click.option('--format', '-f', type=click.Choice(['table', 'json']), default='table', help='Output format')
def list_jobs(state, limit, format):
    """
    List jobs in the queue
    
    Examples:
        queuectl list
        queuectl list --state pending
        queuectl list --state failed --format json
    """
    try:
        # Parse state filter
        state_filter = None
        if state:
            state_filter = JobState(state)

        # Get jobs
        all_jobs = job_store.list_jobs(state_filter)

        if not all_jobs:
            click.echo("No jobs found")
            return

        # Apply limit
        jobs = all_jobs[:limit]

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
                    job.state.value,
                    job.attempts,
                    job.max_retries,
                    job.created_at.strftime('%Y-%m-%d %H:%M:%S') if job.created_at else '-'
                ])

            click.echo(tabulate(
                table_data,
                headers=['ID', 'Command', 'State', 'Attempts', 'Max Retries', 'Created'],
                tablefmt='simple'
            ))

            click.echo(f"\nShowing {len(jobs)} of {len(all_jobs)} job(s)")
            if len(all_jobs) > limit:
                click.echo(f"Use --limit to see more (default is 20)")

    except Exception as e:
        raise click.ClickException(str(e))
