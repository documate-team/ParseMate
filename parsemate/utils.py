from pathlib import Path
from typing import Literal

def check_file_exists(file_path: str) -> bool:
    return Path(file_path).is_file()

def check_file_extension(framework: Literal["fastapi", "express"], file_name: str) -> tuple[bool, str]:
    suffix = Path(file_name).suffix
    match framework:
        case "fastapi":
            return (suffix == '.py', suffix)
        case "express":
            return (suffix == '.js' or suffix == '.ts', suffix)
        case _:
            return (False, suffix)
