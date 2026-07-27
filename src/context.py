from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExtractContext:
    locale: str
    input: Path
    output: Path
    export: tuple[str, ...]
    dynamic_image: str
    fallback_unity_version: str


@dataclass
class ExportContext:
    input: Path
    output: Path
    locale: str
    dynamic_image: str
