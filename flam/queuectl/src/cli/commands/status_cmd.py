"""
Status command - show queue status
"""

import click
from tabulate import tabulate
from src.storage.job_store import job_store
from src.worker.pool import worker_pool
from src.core.models import JobState


@click.command('status')
def status():
    """Show summary of all job states and active workers"""
    try:
        # Get job counts
        counts = job_store.count_by_state()

        # Display job statistics
        click.echo("=" * 50)
        click.echo("JOB QUEUE STATUS")
        click.echo("=" * 50)

        stats = [
            ["Pending", counts.get('pending', 0)],
            ["Processing", counts.get('processing', 0)],
            ["Completed", counts.get('completed', 0)],
            ["Failed", counts.get('failed', 0)],
            ["Dead Letter Queue", counts.get('dlq', 0)],
        ]

        click.echo(tabulate(stats, headers=["State", "Count"], tablefmt="simple"))

        total = sum(counts.values())
        click.echo(f"\nTotal Jobs: {total}")

        # Display worker status
        click.echo("\n" + "=" * 50)
        click.echo("WORKER STATUS")
        click.echo("=" * 50)

        if worker_pool.is_running():
            info = worker_pool.get_worker_info()
            click.echo(f"Active Workers: {info['active']}/{info['total']}")

            for w in info['workers']:
                status_icon = "✓" if w['running'] else "✗"
                job_info = f" [Job: {w['current_job']}]" if w['current_job'] else ""
                click.echo(f"  {status_icon} Worker {w['id']}{job_info}")
        else:
            click.echo("No workers running")

    except Exception as e:
        raise click.ClickException(str(e))
