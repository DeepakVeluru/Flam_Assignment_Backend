"""
Demo script showing QueueCTL capabilities
Run this to see a working example of the job queue system
"""

import subprocess
import time
import sys
from pathlib import Path


def run_cmd(cmd: str):
    """Run a command and print output"""
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=str(Path(__file__).parent.parent))
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def main():
    """Run demo"""
    print("=" * 70)
    print("QUEUECTL DEMO - Job Queue System")
    print("=" * 70)

    print("\n### DEMO 1: Basic Configuration ###")
    run_cmd("python queuectl.py config show")

    print("\n### DEMO 2: Enqueue Jobs ###")
    run_cmd('python queuectl.py enqueue --command "echo Done processing batch 1"')
    run_cmd('python queuectl.py enqueue --command "echo Done processing batch 2"')
    run_cmd('python queuectl.py enqueue --command "sleep 1 && echo Delayed task complete"')

    print("\n### DEMO 3: List Pending Jobs ###")
    run_cmd("python queuectl.py list --state pending")

    print("\n### DEMO 4: Job That Will Fail ###")
    run_cmd('python queuectl.py enqueue --command "exit 1" --max-retries 2')

    print("\n### DEMO 5: Check Current Status ###")
    run_cmd("python queuectl.py status")

    print("\n### DEMO 6: View Help ###")
    print("\nAvailable commands:")
    run_cmd("python queuectl.py --help")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nTo start workers and process jobs, run:")
    print("  python queuectl.py worker start --count 2")
    print("\nIn another terminal, monitor progress with:")
    print("  python queuectl.py status")
    print("\nTo stop workers:")
    print("  python queuectl.py worker stop")


if __name__ == '__main__':
    main()
