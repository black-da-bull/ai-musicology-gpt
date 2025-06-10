from dataclasses import dataclass
from typing import List

@dataclass
class Guardrail:
    rules: List[str]
