"""
Config command - manage configuration
"""

import click
from src.core.config import config


@click.group('config')
def config_cmd():
    """Manage configuration"""
    pass


@config_cmd.command('set')
@click.argument('key')
@click.argument('value')
def config_set(key, value):
    """
    Set a configuration value
    
    Examples:
        queuectl config set max-retries 5
        queuectl config set backoff-base 3
    """
    try:
        # Normalize key
        key = key.replace('-', '_').lower()

        # Type conversion
        if key in ['max_retries', 'backoff_base', 'max_workers', 'worker_timeout']:
            try:
                value = int(value)
            except ValueError:
                raise click.BadParameter(f"{key} must be an integer")

        # Validate values
        if key == 'max_retries' and value < 0:
            raise click.BadParameter("max_retries must be >= 0")
        if key == 'backoff_base' and value < 1:
            raise click.BadParameter("backoff_base must be >= 1")
        if key == 'max_workers' and value < 1:
            raise click.BadParameter("max_workers must be >= 1")

        config.set(key, value)
        click.echo(f"✓ Config updated: {key} = {value}")

    except click.BadParameter:
        raise
    except Exception as e:
        raise click.ClickException(str(e))


@config_cmd.command('get')
@click.argument('key', required=False)
def config_get(key):
    """
    Get configuration value
    
    Examples:
        queuectl config get max-retries
        queuectl config get           # Shows all config
    """
    try:
        if key:
            key = key.replace('-', '_').lower()
            value = config.get(key)
            if value is None:
                click.echo(f"Key '{key}' not found")
            else:
                click.echo(f"{key}: {value}")
        else:
            # Show all config
            all_config = config.get_all()
            click.echo("Current Configuration:")
            click.echo("=" * 40)
            for k, v in all_config.items():
                click.echo(f"  {k}: {v}")

    except Exception as e:
        raise click.ClickException(str(e))


@config_cmd.command('reset')
@click.confirmation_option(prompt='Are you sure you want to reset to defaults?')
def config_reset():
    """Reset configuration to defaults"""
    try:
        config.reset()
        click.echo("✓ Configuration reset to defaults")

    except Exception as e:
        raise click.ClickException(str(e))


@config_cmd.command('show')
def config_show():
    """Show all configuration and paths"""
    try:
        click.echo("=" * 60)
        click.echo("CONFIGURATION")
        click.echo("=" * 60)
        all_config = config.get_all()
        for k, v in all_config.items():
            click.echo(f"  {k}: {v}")

        click.echo("\n" + "=" * 60)
        click.echo("STORAGE PATHS")
        click.echo("=" * 60)
        click.echo(f"  Config Dir: {config.config_dir}")
        click.echo(f"  Jobs File: {config.jobs_file}")
        click.echo(f"  DLQ File: {config.dlq_file}")
        click.echo(f"  PID File: {config.pid_file}")

    except Exception as e:
        raise click.ClickException(str(e))
