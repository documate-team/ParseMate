from abc import ABC, abstractmethod
import ast
from typing import Any

class Parser(ABC):

    @abstractmethod
    def parse(self, file_content: str) -> ast.Module | None:
        ...


    @abstractmethod
    def extract_metadata(self) -> dict[str, Any]:
        ...
