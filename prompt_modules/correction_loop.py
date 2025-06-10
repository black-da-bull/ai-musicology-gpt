from dataclasses import dataclass

@dataclass
class CorrectionLoop:
    max_iterations: int
    criteria: str
