#!/usr/bin/env python3
"""
Quick Start Guide - Interactive QueueCTL Demo
Run this script for a guided introduction to QueueCTL
"""

import subprocess
import time
import os
from pathlib import Path


def run_cmd(cmd: str, show_output: bool = True) -> str:
    """Run a command and return output"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent)
    )
    if show_output and result.stdout:
        print(result.stdout)
    return result.stdout


def pause(msg: str = "Press Enter to continue..."):
    """Pause and wait for user input"""
    try:
        input(f"\n{msg}\n")
    except KeyboardInterrupt:
        print("\nQuick start cancelled.")
        exit(0)


def main():
    """Interactive quick start guide"""
    print("=" * 70)
    print("QUEUECTL - QUICK START GUIDE")
    print("=" * 70)

    print("\n📚 Welcome to QueueCTL!")
    print("This interactive guide will show you the basics.")

    pause()

    # Step 1: Configuration
    print("\n1️⃣  CONFIGURATION")
    print("-" * 70)
    print("Let's check the current configuration:")
    run_cmd("python queuectl.py config get")
    pause()

    # Step 2: Enqueue
    print("\n2️⃣  ENQUEUING JOBS")
    print("-" * 70)
    print("Adding some jobs to the queue:\n")

    print("Job 1: Simple echo")
    run_cmd('python queuectl.py enqueue --command "echo Job 1: Hello from QueueCTL"')

    print("\nJob 2: Delayed task")
    run_cmd('python queuectl.py enqueue --command "sleep 1 && echo Job 2: Done sleeping"')

    print("\nJob 3: Will fail and retry")
    run_cmd('python queuectl.py enqueue --command "exit 1" --max-retries 2')

    pause()

    # Step 3: List jobs
    print("\n3️⃣  LISTING JOBS")
    print("-" * 70)
    print("Let's see all pending jobs:\n")
    run_cmd("python queuectl.py list --state pending")

    pause()

    # Step 4: Status
    print("\n4️⃣  CHECKING STATUS")
    print("-" * 70)
    print("Current queue status:\n")
    run_cmd("python queuectl.py status")

    pause()

    # Step 5: Start workers
    print("\n5️⃣  STARTING WORKERS")
    print("-" * 70)
    print("Now we'll start workers to process the jobs.")
    print("Workers will process jobs and then exit.")
    print("(Workers will stop after processing all pending jobs)\n")

    # Create a wrapper script to start workers for limited time
    worker_cmd = """python -c "
import subprocess
import time
import sys
import threading

# Start workers in background
proc = subprocess.Popen([sys.executable, 'queuectl.py', 'worker', 'start', '--count', '2'], 
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Wait for 5 seconds or until jobs are done
time.sleep(5)

# Try to stop gracefully
try:
    subprocess.run([sys.executable, 'queuectl.py', 'worker', 'stop'], timeout=3)
except:
    pass
"
"""

    run_cmd(worker_cmd, show_output=False)

    print("✓ Workers processed jobs and stopped")
    pause()

    # Step 6: Check results
    print("\n6️⃣  CHECKING RESULTS")
    print("-" * 70)
    print("Let's see what happened:\n")

    print("Completed jobs:")
    run_cmd("python queuectl.py list --state completed")

    print("\nFailed jobs (to be retried):")
    run_cmd("python queuectl.py list --state failed")

    pause()

    # Step 7: DLQ
    print("\n7️⃣  DEAD LETTER QUEUE")
    print("-" * 70)
    print("Let's check the Dead Letter Queue:\n")
    run_cmd("python queuectl.py dlq list")

    pause()

    # Step 8: Help
    print("\n8️⃣  GETTING HELP")
    print("-" * 70)
    print("All commands have detailed help:\n")
    print("Try these:")
    print("  python queuectl.py --help")
    print("  python queuectl.py enqueue --help")
    print("  python queuectl.py worker --help")
    print("  python queuectl.py list --help")
    print("  python queuectl.py dlq --help")

    pause()

    # Final summary
    print("\n" + "=" * 70)
    print("✅ QUICK START COMPLETE!")
    print("=" * 70)

    print("\n📖 Key Commands to Remember:")
    print("  enqueue   - Add jobs: queuectl enqueue --command 'your_command'")
    print("  worker    - Manage workers: queuectl worker start/stop")
    print("  status    - View queue status: queuectl status")
    print("  list      - List jobs: queuectl list --state pending")
    print("  dlq       - DLQ operations: queuectl dlq list/retry")
    print("  config    - Manage config: queuectl config set/get")

    print("\n📚 Documentation:")
    print("  README.md      - Comprehensive usage guide")
    print("  ARCHITECTURE.md - System design and internals")

    print("\n💡 Next Steps:")
    print("  1. Read the full README.md for all features")
    print("  2. Try the test script: python tests/test_flows.py")
    print("  3. Build your own job workflow!")

    print("\n🚀 Happy queuing!\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nQuick start cancelled.")
