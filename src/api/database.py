import math
from typing import Type, Any, List, Dict

from tortoise import Model

from .schemas import PaginationSchema


async def pagination(
    model: Type[Model], page: int, size: int, orderings: List[str], filters: Dict[str, Any]
) -> PaginationSchema:
    offset = (page - 1) * size
    limit = size
    total_items = await model.all().count()
    total_pages = math.ceil(total_items / size)
    results = await model.all().offset(offset).limit(limit).filter(**filters).order_by(*orderings)
    return PaginationSchema(
        page=page,
        size=size,
        total_pages=total_pages,
        total_items=total_items,
        results=results,
    )
