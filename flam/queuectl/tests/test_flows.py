"""
Integration tests and flow validation
Run this script to test all core QueueCTL functionality
"""

import json
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime


class TestRunner:
    """Test runner for QueueCTL"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.test_results = []

    def run_command(self, cmd: str) -> tuple[int, str, str]:
        """Run a CLI command and return exit code, stdout, stderr"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(Path(__file__).parent.parent)
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)

    def test(self, name: str, condition: bool, message: str = ""):
        """Record a test result"""
        if condition:
            self.passed += 1
            status = "✓ PASS"
        else:
            self.failed += 1
            status = "✗ FAIL"

        msg = f"{status}: {name}"
        if message:
            msg += f" - {message}"

        print(msg)
        self.test_results.append((name, condition, message))

    def report(self):
        """Print test summary"""
        print("\n" + "=" * 70)
        print(f"TEST SUMMARY: {self.passed} passed, {self.failed} failed")
        print("=" * 70)
        return self.failed == 0


def test_enqueue_basic():
    """Test basic job enqueuing"""
    print("\n--- TEST: Basic Job Enqueuing ---")
    runner = TestRunner()

    # Test 1: Enqueue with command option
    code, out, err = runner.run_command('python queuectl.py enqueue --command "echo test"')
    success = code == 0 and ("Job enqueued" in out or "Job enqueued" in err)
    runner.test(
        "Enqueue with --command",
        success,
        f"Code: {code}, Output captured"
    )

    # Test 2: Enqueue with JSON
    json_job = json.dumps({
        "id": "test-job-1",
        "command": "echo hello",
        "max_retries": 3
    })
    code, out, err = runner.run_command(f'python queuectl.py enqueue \'{json_job}\'')
    success = code == 0 and ("Job enqueued" in out or "Job enqueued" in err)
    runner.test(
        "Enqueue with JSON",
        success,
        f"Code: {code}, Output captured"
    )

    return runner


def test_list_jobs():
    """Test job listing"""
    print("\n--- TEST: List Jobs ---")
    runner = TestRunner()

    # Test 1: List all jobs
    code, out, err = runner.run_command('python queuectl.py list')
    runner.test(
        "List all jobs",
        code == 0,
        f"Jobs listed: {out[:100]}"
    )

    # Test 2: List pending jobs
    code, out, err = runner.run_command('python queuectl.py list --state pending')
    runner.test(
        "List pending jobs",
        code == 0,
        f"Output: {out[:100]}"
    )

    # Test 3: List with JSON format
    code, out, err = runner.run_command('python queuectl.py list --format json')
    runner.test(
        "List with JSON format",
        code == 0 and (out.startswith('[') or out.strip() == 'No jobs found'),
        f"Valid JSON: {out[:100]}"
    )

    return runner


def test_config_management():
    """Test configuration management"""
    print("\n--- TEST: Configuration Management ---")
    runner = TestRunner()

    # Test 1: Get default config
    code, out, err = runner.run_command('python queuectl.py config get')
    runner.test(
        "Get all config",
        code == 0 and "max_retries" in out,
        f"Config shown"
    )

    # Test 2: Set config value
    code, out, err = runner.run_command('python queuectl.py config set max-retries 5')
    success = code == 0 and ("Config updated" in out or "Config updated" in err)
    runner.test(
        "Set config value",
        success,
        f"Config set successfully"
    )

    # Test 3: Get specific config
    code, out, err = runner.run_command('python queuectl.py config get max-retries')
    runner.test(
        "Get specific config",
        code == 0 and ("5" in out or "max_retries" in out),
        f"Value retrieved"
    )

    # Test 4: Config show (with paths)
    code, out, err = runner.run_command('python queuectl.py config show')
    runner.test(
        "Show config with paths",
        code == 0 and "STORAGE PATHS" in out,
        f"Paths shown"
    )

    return runner


def test_status():
    """Test status command"""
    print("\n--- TEST: Status Command ---")
    runner = TestRunner()

    # Test 1: Show status
    code, out, err = runner.run_command('python queuectl.py status')
    runner.test(
        "Show status",
        code == 0 and "JOB QUEUE STATUS" in out,
        f"Status shown: {out[:150]}"
    )

    # Test 2: Status includes job counts
    code, out, err = runner.run_command('python queuectl.py status')
    runner.test(
        "Status shows job counts",
        code == 0 and ("Pending" in out or "pending" in out),
        f"Job states shown"
    )

    return runner


def test_dlq_operations():
    """Test Dead Letter Queue operations"""
    print("\n--- TEST: Dead Letter Queue ---")
    runner = TestRunner()

    # Test 1: List DLQ (should be empty or show jobs)
    code, out, err = runner.run_command('python queuectl.py dlq list')
    runner.test(
        "List DLQ",
        code == 0,
        f"Output: {out[:100]}"
    )

    # Test 2: DLQ show with JSON
    code, out, err = runner.run_command('python queuectl.py dlq list --format json')
    runner.test(
        "DLQ list as JSON",
        code == 0 and (out.startswith('[') or "empty" in out.lower()),
        f"Valid JSON: {out[:100]}"
    )

    return runner


def test_worker_info():
    """Test worker info command"""
    print("\n--- TEST: Worker Info ---")
    runner = TestRunner()

    # Test 1: Worker info (no workers running)
    code, out, err = runner.run_command('python queuectl.py worker info')
    runner.test(
        "Worker info when no workers",
        code == 0 and ("No workers" in out or "0" in out),
        f"Output: {out[:100]}"
    )

    return runner


def test_help_commands():
    """Test help for all commands"""
    print("\n--- TEST: Help Commands ---")
    runner = TestRunner()

    commands = [
        'python queuectl.py --help',
        'python queuectl.py enqueue --help',
        'python queuectl.py worker --help',
        'python queuectl.py status --help',
        'python queuectl.py list --help',
        'python queuectl.py dlq --help',
        'python queuectl.py config --help',
    ]

    for cmd in commands:
        code, out, err = runner.run_command(cmd)
        cmd_name = cmd.split()[-2] if '--help' in cmd else 'main'
        runner.test(
            f"Help for {cmd_name}",
            code == 0 and len(out) > 50,
            f"Help text shown"
        )

    return runner


def test_error_handling():
    """Test error handling"""
    print("\n--- TEST: Error Handling ---")
    runner = TestRunner()

    # Test 1: Invalid state filter
    code, out, err = runner.run_command('python queuectl.py list --state invalid')
    runner.test(
        "Reject invalid state",
        code != 0,
        f"Error shown: {err[:100]}"
    )

    # Test 2: Enqueue without args
    code, out, err = runner.run_command('python queuectl.py enqueue')
    runner.test(
        "Enqueue requires args",
        code != 0,
        f"Error shown"
    )

    # Test 3: Invalid config value type
    code, out, err = runner.run_command('python queuectl.py config set max-retries abc')
    runner.test(
        "Reject non-integer config",
        code != 0,
        f"Error shown"
    )

    return runner


def main():
    """Run all tests"""
    print("=" * 70)
    print("QUEUECTL - INTEGRATION TEST SUITE")
    print("=" * 70)

    # Cleanup any existing data for clean test
    print("\nPreparing test environment...")

    all_runners = []

    # Run test suites
    all_runners.append(test_enqueue_basic())
    all_runners.append(test_list_jobs())
    all_runners.append(test_config_management())
    all_runners.append(test_status())
    all_runners.append(test_dlq_operations())
    all_runners.append(test_worker_info())
    all_runners.append(test_help_commands())
    all_runners.append(test_error_handling())

    # Print final summary
    print("\n" + "=" * 70)
    total_passed = sum(r.passed for r in all_runners)
    total_failed = sum(r.failed for r in all_runners)
    total_tests = total_passed + total_failed

    print(f"FINAL RESULTS: {total_passed}/{total_tests} tests passed")

    if total_failed == 0:
        print("✓ ALL TESTS PASSED!")
        print("=" * 70)
        return 0
    else:
        print(f"✗ {total_failed} test(s) failed")
        print("=" * 70)
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
