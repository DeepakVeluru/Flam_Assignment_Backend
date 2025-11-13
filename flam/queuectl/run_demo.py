#!/usr/bin/env python3
"""
Complete QueueCTL Demo - Shows all major features
"""

import subprocess
import time
from pathlib import Path


def cmd(command: str) -> str:
    """Execute command and return output"""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent)
    )
    return result.stdout + result.stderr


def main():
    print("=" * 70)
    print("QUEUECTL - COMPLETE DEMO")
    print("=" * 70)

    print("\n1️⃣  VERSION CHECK")
    print("-" * 70)
    print(cmd("python queuectl.py --version"))

    print("\n2️⃣  ENQUEUE JOBS")
    print("-" * 70)
    print("Adding 3 jobs to the queue...")
    print(cmd('python queuectl.py enqueue --command "echo Job 1: Task completed"'))
    print(cmd('python queuectl.py enqueue --command "sleep 1 && echo Job 2: Delayed task"'))
    print(cmd('python queuectl.py enqueue --command "exit 1" --max-retries 2'))

    print("\n3️⃣  LIST PENDING JOBS")
    print("-" * 70)
    print(cmd("python queuectl.py list --state pending"))

    print("\n4️⃣  CHECK STATUS BEFORE WORKERS")
    print("-" * 70)
    print(cmd("python queuectl.py status"))

    print("\n5️⃣  CONFIGURATION")
    print("-" * 70)
    print("Current config:")
    print(cmd("python queuectl.py config get"))

    print("\n6️⃣  WORKER COMMANDS")
    print("-" * 70)
    print("Starting worker...")
    worker_proc = subprocess.Popen(
        "python queuectl.py worker start --count 1",
        shell=True,
        cwd=str(Path(__file__).parent),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Let worker process jobs for 10 seconds
    time.sleep(10)

    print("Stopping worker...")
    try:
        worker_proc.terminate()
        worker_proc.wait(timeout=5)
    except:
        worker_proc.kill()

    print("✓ Worker stopped")

    print("\n7️⃣  FINAL STATUS")
    print("-" * 70)
    print(cmd("python queuectl.py status"))

    print("\n8️⃣  COMPLETED JOBS")
    print("-" * 70)
    print(cmd("python queuectl.py list --state completed"))

    print("\n9️⃣  FAILED JOBS (awaiting retry)")
    print("-" * 70)
    print(cmd("python queuectl.py list --state failed"))

    print("\n🔟 DEAD LETTER QUEUE")
    print("-" * 70)
    print(cmd("python queuectl.py dlq list"))

    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)
    print("\n📚 Key Features Demonstrated:")
    print("  ✓ Job enqueuing with custom commands")
    print("  ✓ Job listing and filtering")
    print("  ✓ Queue status monitoring")
    print("  ✓ Worker processing")
    print("  ✓ Job state transitions")
    print("  ✓ Retry logic")
    print("  ✓ Configuration management")
    print("  ✓ DLQ operations")
    print("\n📖 Next Steps:")
    print("  - Read README.md for comprehensive guide")
    print("  - Check ARCHITECTURE.md for design details")
    print("  - Run test suite: python tests/test_flows.py")
    print("  - Explore: python queuectl.py <command> --help")


if __name__ == '__main__':
    main()
