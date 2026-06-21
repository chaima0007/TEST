from dataclasses import dataclass

@dataclass
class KBResult:
    id: str
    slug: str
    type: str
    score: float
    snippet: str
    source: str
