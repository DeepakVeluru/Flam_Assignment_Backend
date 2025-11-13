"""
Unit tests for core components
"""

import json
import tempfile
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.models import Job, JobState
from src.core.executor import JobExecutor
from src.core.config import config


def test_job_model():
    """Test Job model creation and serialization"""
    print("Test: Job Model")

    # Create job
    job = Job(command="echo hello")
    assert job.id is not None
    assert job.state == JobState.PENDING
    assert job.attempts == 0

    # Serialize to dict
    data = job.to_dict()
    assert data['command'] == "echo hello"
    assert data['state'] == "pending"

    # Deserialize from dict
    job2 = Job.from_dict(data)
    assert job2.id == job.id
    assert job2.command == job.command

    print("  ✓ Job model works correctly")


def test_job_executor():
    """Test JobExecutor"""
    print("Test: Job Executor")

    executor = JobExecutor()

    # Test successful execution
    job = Job(command='echo "success"')
    success, output, error = executor.execute(job)
    assert success is True
    assert "success" in output

    # Test failed execution
    job = Job(command='exit 1')
    success, output, error = executor.execute(job)
    assert success is False
    assert "exit code" in error

    # Test command not found
    job = Job(command='nonexistentcommand12345')
    success, output, error = executor.execute(job)
    assert success is False

    print("  ✓ Job executor works correctly")


def test_backoff_calculation():
    """Test exponential backoff calculation"""
    print("Test: Exponential Backoff")

    executor = JobExecutor()

    # Create jobs with different attempt counts
    job1 = Job(command="echo test", attempts=0)
    job2 = Job(command="echo test", attempts=1)
    job3 = Job(command="echo test", attempts=2)

    backoff1 = executor.calculate_backoff(job1)
    backoff2 = executor.calculate_backoff(job2)
    backoff3 = executor.calculate_backoff(job3)

    # With base 2:
    # 2^0 = 1 sec, 2^1 = 2 sec, 2^2 = 4 sec
    # Each should be progressively longer
    assert backoff2 > backoff1
    assert backoff3 > backoff2

    print("  ✓ Exponential backoff calculation works")


def test_config():
    """Test configuration management"""
    print("Test: Configuration")

    # Get default
    default_retries = config.get('max_retries')
    assert default_retries is not None

    # Set and get
    original = config.get('max_retries')
    config.set('max_retries', 99)
    assert config.get('max_retries') == 99

    # Restore
    config.set('max_retries', original)
    assert config.get('max_retries') == original

    print("  ✓ Configuration works correctly")


def test_job_state_enum():
    """Test JobState enumeration"""
    print("Test: JobState Enum")

    states = [
        JobState.PENDING,
        JobState.PROCESSING,
        JobState.COMPLETED,
        JobState.FAILED,
        JobState.DEAD
    ]

    # All states should have values
    for state in states:
        assert state.value in ['pending', 'processing', 'completed', 'failed', 'dead']

    # Creation from value
    assert JobState('pending') == JobState.PENDING
    assert JobState('dead') == JobState.DEAD

    print("  ✓ JobState enum works correctly")


def main():
    """Run all unit tests"""
    print("\n" + "=" * 50)
    print("UNIT TESTS")
    print("=" * 50 + "\n")

    try:
        test_job_model()
        test_job_executor()
        test_backoff_calculation()
        test_config()
        test_job_state_enum()

        print("\n" + "=" * 50)
        print("✓ ALL UNIT TESTS PASSED")
        print("=" * 50)
        return 0

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
