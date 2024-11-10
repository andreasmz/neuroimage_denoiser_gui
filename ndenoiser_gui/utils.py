from enum import Enum
import uuid

class FileStatus(Enum):
    QUEUED = "Queued"
    RUNNING = "Running"
    FINISHED = "Finished"
    FAILED = "Failed"

class QueuedFile:
    def __init__(self, path):
        self.path = path
        self.id = str(uuid.uuid4())
        self.status: FileStatus = FileStatus.QUEUED