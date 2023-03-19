from enum import Enum



class JobStatus(Enum):
    """Class for job status enumerated type."""

    INITIALIZING = "INITIALIZING"
    QUEUED = "QUEUED"
    VALIDATING = "VALIDATING"
    RUNNING = "RUNNING"
    CANCELLED = "CANCELLED"
    DONE = "DONE"
    ERROR = "ERROR"

JOB_FINAL_STATES = (JobStatus.DONE.value, JobStatus.CANCELLED.value, JobStatus.ERROR.value)
