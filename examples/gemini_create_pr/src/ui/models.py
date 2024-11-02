from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class InitialInput:
    repo_path: str
    task: str

@dataclass
class FileChange:
    file_path: str
    content: str

@dataclass
class SolutionValidation:
    approved: bool
    feedback: Optional[str] = None

@dataclass
class WorkflowResult:
    files_to_create_or_update: List[FileChange]
    chat_history: List[Any]

@dataclass
class PrInfoValidation:
    approved: bool
    feedback: Optional[str] = None