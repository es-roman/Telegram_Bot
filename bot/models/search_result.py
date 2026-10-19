from dataclasses import dataclass


@dataclass
class SearchResult:
    title: str
    url: str
    source: str
    description: str | None = None
    language: str | None = None
    stars: int | None = None
    score: int | None = None
    answers: int | None = None
    status: str | None = None
