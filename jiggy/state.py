class State:
    """State values."""

    NONE = "NONE"
    SCHEDULED = "SCHEDULED"
    PENDING = "PENDING"
    PENDING_RETRY = "PENDING_RETRY"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    FAILED_UPSTREAM = "FAILED_UPSTREAM"
    SKIPPED = "SKIPPED"

    @classmethod
    def all(cls):
        return set(k for k in cls.__dict__ if k == k.upper())

    @classmethod
    def pending(cls):
        return {[cls.PENDING, cls.PENDING_RETRY, cls.SCHEDULED]}

    @classmethod
    def running(cls):
        return {[cls.RUNNING]}

    @classmethod
    def finished(cls):
        return {[cls.SUCCESS, cls.FAILED, cls.SKIPPED]}
