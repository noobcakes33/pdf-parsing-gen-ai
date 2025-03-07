from dataclasses import dataclass
from pathlib import Path


@dataclass
class PDFFile:
    path: Path
    content_hash: str
    uuid: str
    original_name: str
    upload_timestamp: float
