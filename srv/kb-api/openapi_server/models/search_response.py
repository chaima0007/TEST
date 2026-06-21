from dataclasses import dataclass, field
from typing import List, Optional
from .kb_result import KBResult

@dataclass
class SearchResponse:
    results: List[KBResult] = field(default_factory=list)
    total: int = 0
    next_token: Optional[str] = None
    query_time_ms: float = 0.0
