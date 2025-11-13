#!/usr/bin/env python3
"""
QueueCTL - CLI-based background job queue system
Main entry point for the CLI application
"""

import click
from src.cli.commands import enqueue_cmd, worker_cmd, status_cmd, list_cmd, dlq_cmd, config_cmd


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """QueueCTL - Background Job Queue Management System"""
    pass


# Register commands
cli.add_command(enqueue_cmd.enqueue)
cli.add_command(worker_cmd.worker)
cli.add_command(status_cmd.status)
cli.add_command(list_cmd.list_jobs)
cli.add_command(dlq_cmd.dlq)
cli.add_command(config_cmd.config_cmd)


if __name__ == '__main__':
    cli()
