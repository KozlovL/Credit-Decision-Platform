from common.schemas.product import ProductRead
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import PRODUCTS_PREFIX, PRODUCTS_TAG, ClientType
from app.core.db import get_session
from app.models.products import Products

router = APIRouter(prefix=PRODUCTS_PREFIX, tags=[PRODUCTS_TAG])


@router.get(
    '',
    response_model=list[ProductRead],
    summary='Получение списка продуктов с фильтрацией по типу пользователя'
)
async def get_products(
        flow_type: ClientType | None = Query(None),
        session: AsyncSession = Depends(get_session)
) -> list[ProductRead]:
    query = select(Products)
    if flow_type is not None:
        query = query.where(Products.flow_type == flow_type)
    products = await session.execute(query)
    return products.scalars().all()  # type: ignore[return-value]
