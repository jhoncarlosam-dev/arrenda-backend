from typing import Generic, List, TypeVar
from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams:
    def __init__(
        self,
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=20, ge=1, le=100, description="Max records to return (1-100)"),
    ):
        self.skip = skip
        self.limit = limit


class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int
    limit: int
