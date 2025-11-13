#!/usr/bin/env python3
"""
QueueCTL - Complete Demo with All Commands
Copy and paste these commands to demonstrate the system
"""

import subprocess
import time
from pathlib import Path


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def run_and_show(cmd, description):
    """Run command and show both command and output"""
    print(f"📌 {description}")
    print(f"Command: {cmd}\n")
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent)
    )
    print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr}")
    input("Press Enter to continue...\n")
    return result


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    QUEUECTL - COMPLETE DEMONSTRATION                        ║
║                                                                              ║
║                Copy and paste these commands to see QueueCTL in action      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    input("Press Enter to start the demo...\n")

    # =========================================================================
    print_section("1. CHECK VERSION & HELP")
    # =========================================================================
    run_and_show(
        "python queuectl.py --version",
        "Show QueueCTL version"
    )

    run_and_show(
        "python queuectl.py --help",
        "Show main help menu"
    )

    # =========================================================================
    print_section("2. VIEW CURRENT CONFIGURATION")
    # =========================================================================
    run_and_show(
        "python queuectl.py config show",
        "Show all configuration and storage paths"
    )

    run_and_show(
        "python queuectl.py config get",
        "Get specific configuration values"
    )

    # =========================================================================
    print_section("3. ENQUEUE JOBS - SIMPLE COMMANDS")
    # =========================================================================
    run_and_show(
        'python queuectl.py enqueue --command "echo Task 1: Hello World"',
        "Enqueue a simple echo command"
    )

    run_and_show(
        'python queuectl.py enqueue --command "echo Task 2: Processing data"',
        "Enqueue another simple task"
    )

    run_and_show(
        'python queuectl.py enqueue --command "powershell Write-Host Task 3: PowerShell command"',
        "Enqueue a PowerShell command"
    )

    # =========================================================================
    print_section("4. ENQUEUE JOBS - WITH RETRIES")
    # =========================================================================
    run_and_show(
        'python queuectl.py enqueue --command "echo Task 4: Will be retried" --max-retries 5',
        "Enqueue with custom max retries"
    )

    run_and_show(
        'python queuectl.py enqueue --command "exit 1" --max-retries 3',
        "Enqueue a job that will fail and retry"
    )

    # =========================================================================
    print_section("5. LIST JOBS - DIFFERENT STATES")
    # =========================================================================
    run_and_show(
        "python queuectl.py list",
        "List all jobs (table format)"
    )

    run_and_show(
        "python queuectl.py list --state pending",
        "List only PENDING jobs"
    )

    run_and_show(
        "python queuectl.py list --state pending --format json",
        "List pending jobs in JSON format"
    )

    # =========================================================================
    print_section("6. CHECK QUEUE STATUS")
    # =========================================================================
    run_and_show(
        "python queuectl.py status",
        "Show queue status and worker information"
    )

    # =========================================================================
    print_section("7. START WORKERS - PROCESS JOBS")
    # =========================================================================
    print("📌 Starting workers for 15 seconds to process jobs...\n")
    print("Command: python queuectl.py worker start --count 2\n")
    
    proc = subprocess.Popen(
        "python queuectl.py worker start --count 2",
        shell=True,
        cwd=str(Path(__file__).parent),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("✓ Workers started (2 workers processing jobs in parallel)\n")
    time.sleep(8)
    
    print("Checking status while workers are running...\n")
    result = subprocess.run(
        "python queuectl.py status",
        shell=True,
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent)
    )
    print(result.stdout)
    
    time.sleep(7)
    
    print("Stopping workers gracefully...\n")
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except:
        proc.kill()
    
    print("✓ Workers stopped\n")
    input("Press Enter to continue...\n")

    # =========================================================================
    print_section("8. CHECK RESULTS AFTER PROCESSING")
    # =========================================================================
    run_and_show(
        "python queuectl.py status",
        "Show updated queue status"
    )

    run_and_show(
        "python queuectl.py list --state completed",
        "List completed jobs"
    )

    run_and_show(
        "python queuectl.py list --state failed",
        "List failed jobs (waiting for retry)"
    )

    # =========================================================================
    print_section("9. DEAD LETTER QUEUE - FAILED JOBS")
    # =========================================================================
    run_and_show(
        "python queuectl.py dlq list",
        "View Dead Letter Queue (permanently failed jobs)"
    )

    # Try to get a DLQ job if one exists
    result = subprocess.run(
        "python queuectl.py dlq list --format json",
        shell=True,
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent)
    )
    
    if "[" in result.stdout and "{" in result.stdout:
        import json
        try:
            jobs = json.loads(result.stdout)
            if jobs and len(jobs) > 0:
                job_id = jobs[0].get('id', '')
                if job_id:
                    run_and_show(
                        f'python queuectl.py dlq details {job_id}',
                        "View details of a failed job in DLQ"
                    )

                    run_and_show(
                        f'python queuectl.py dlq retry {job_id}',
                        "Retry a failed job from DLQ"
                    )

                    run_and_show(
                        "python queuectl.py list --state pending",
                        "Verify the job is back in queue as PENDING"
                    )
        except:
            pass

    # =========================================================================
    print_section("10. CONFIGURATION - CUSTOMIZE SETTINGS")
    # =========================================================================
    run_and_show(
        "python queuectl.py config set max-retries 5",
        "Change max retries to 5"
    )

    run_and_show(
        "python queuectl.py config set backoff-base 3",
        "Change backoff base to 3 (exponential backoff: 3^attempts)"
    )

    run_and_show(
        "python queuectl.py config get",
        "View updated configuration"
    )

    # =========================================================================
    print_section("11. WORKER COMMANDS - DETAILED")
    # =========================================================================
    run_and_show(
        "python queuectl.py worker --help",
        "Show worker command help"
    )

    run_and_show(
        "python queuectl.py worker info",
        "Show worker information (when no workers running)"
    )

    # =========================================================================
    print_section("12. COMPLETE WORKFLOW EXAMPLE")
    # =========================================================================
    print("📌 Complete workflow: Enqueue → Process → Monitor\n")
    
    print("Step 1: Enqueue 3 jobs")
    run_and_show(
        'python queuectl.py enqueue --command "echo Workflow job 1"',
        "Enqueue job 1"
    )
    
    run_and_show(
        'python queuectl.py enqueue --command "echo Workflow job 2"',
        "Enqueue job 2"
    )
    
    run_and_show(
        'python queuectl.py enqueue --command "echo Workflow job 3"',
        "Enqueue job 3"
    )

    run_and_show(
        "python queuectl.py status",
        "Check status before processing"
    )

    print("\nStep 2: Start worker and process jobs (10 seconds)")
    proc = subprocess.Popen(
        "python queuectl.py worker start --count 1",
        shell=True,
        cwd=str(Path(__file__).parent),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("✓ Worker started\n")
    time.sleep(10)
    
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except:
        proc.kill()
    
    print("✓ Worker stopped\n")

    run_and_show(
        "python queuectl.py status",
        "Check status after processing"
    )

    run_and_show(
        "python queuectl.py list --state completed",
        "View completed jobs"
    )

    # =========================================================================
    print_section("13. HELPFUL COMMANDS FOR TROUBLESHOOTING")
    # =========================================================================
    
    print("""
Here are helpful commands for troubleshooting and monitoring:

📋 MONITORING
  python queuectl.py status                      # Overall status
  python queuectl.py list                        # All jobs
  python queuectl.py list --state pending        # Pending jobs
  python queuectl.py list --state processing     # Processing jobs
  python queuectl.py list --state completed      # Completed jobs
  python queuectl.py list --state failed         # Failed jobs (retry pending)

👷 WORKER MANAGEMENT
  python queuectl.py worker start --count 2      # Start 2 workers
  python queuectl.py worker start --count 4      # Start 4 workers
  python queuectl.py worker info                 # Worker status
  python queuectl.py worker stop                 # Stop workers

📨 DEAD LETTER QUEUE
  python queuectl.py dlq list                    # View DLQ jobs
  python queuectl.py dlq details <job-id>        # Job details
  python queuectl.py dlq retry <job-id>          # Retry job
  python queuectl.py dlq remove <job-id>         # Remove job

⚙️ CONFIGURATION
  python queuectl.py config show                 # Show all config
  python queuectl.py config set max-retries 5    # Set max retries
  python queuectl.py config set backoff-base 3   # Set backoff base
  python queuectl.py config get                  # Get all values
  python queuectl.py config reset                # Reset to defaults

📄 OUTPUT FORMATS
  python queuectl.py list --format json          # JSON output
  python queuectl.py dlq list --format json      # DLQ as JSON

💡 HELP & DOCUMENTATION
  python queuectl.py --help                      # Main help
  python queuectl.py <command> --help            # Command help
  cat README.md                                  # Full documentation
  cat GETTING_STARTED.md                         # Quick start
  cat ARCHITECTURE.md                            # System design
    """)

    input("Press Enter to see summary...\n")

    # =========================================================================
    print_section("DEMONSTRATION COMPLETE!")
    # =========================================================================
    
    print("""
✅ You've seen QueueCTL in action with:

  ✓ Job enqueuing (simple and with retries)
  ✓ Job listing (different states and formats)
  ✓ Queue status monitoring
  ✓ Worker processing (parallel job execution)
  ✓ Dead Letter Queue management
  ✓ Configuration management
  ✓ Complete workflow example

📚 Next Steps:
  1. Read README.md for comprehensive documentation
  2. Try the commands above in your own workflow
  3. Check GETTING_STARTED.md for more examples
  4. Review ARCHITECTURE.md to understand the design

💻 Quick Command Template:
    python queuectl.py enqueue --command "your command here"
    python queuectl.py worker start --count 2
    python queuectl.py status
    python queuectl.py worker stop

🚀 Happy Queuing!
    """)

    print("=" * 80 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user.")
    except Exception as e:
        print(f"\nError during demo: {e}")


"""
ALTERNATIVE: RUN THESE COMMANDS MANUALLY IN YOUR TERMINAL

Navigate to: cd c:\Users\deepa\Documents\flam\queuectl

Then copy/paste these commands one by one:

1. python queuectl.py --version

2. python queuectl.py config show

3. python queuectl.py enqueue --command "echo Job 1"

4. python queuectl.py enqueue --command "echo Job 2"

5. python queuectl.py enqueue --command "exit 1" --max-retries 2

6. python queuectl.py list

7. python queuectl.py status

8. python queuectl.py worker start --count 2
   (Let it run for 15 seconds, then press Ctrl+C)

9. python queuectl.py status

10. python queuectl.py list --state completed

11. python queuectl.py dlq list

12. python queuectl.py config set max-retries 5

13. python queuectl.py config get

That's it! You've demonstrated the complete QueueCTL system.
"""
