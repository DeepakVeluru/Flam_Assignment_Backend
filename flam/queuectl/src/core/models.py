"""
Job model definition
"""

from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid


class JobState(str, Enum):
    """Job state enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD = "dead"


class Job(BaseModel):
    """Job model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    command: str
    state: JobState = JobState.PENDING
    attempts: int = 0
    max_retries: int = 3
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    output: Optional[str] = None
    error: Optional[str] = None
    next_retry_at: Optional[datetime] = None

    class Config:
        use_enum_values = False

    def to_dict(self):
        """Convert to dictionary"""
        data = self.dict()
        data['created_at'] = self.created_at.isoformat() if self.created_at else None
        data['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        data['next_retry_at'] = self.next_retry_at.isoformat() if self.next_retry_at else None
        data['state'] = self.state.value if isinstance(self.state, JobState) else self.state
        return data

    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        if isinstance(data.get('state'), str):
            data['state'] = JobState(data['state'])
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if isinstance(data.get('updated_at'), str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        if data.get('next_retry_at') and isinstance(data['next_retry_at'], str):
            data['next_retry_at'] = datetime.fromisoformat(data['next_retry_at'])
        return cls(**data)
