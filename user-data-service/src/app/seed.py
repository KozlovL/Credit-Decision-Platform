import asyncio
import logging
from json import load

from sqlalchemy import select

from app.constants import PIONEER_PRODUCTS_JSON_PATH, REPEATER_PRODUCTS_JSON_PATH
from app.core.db import async_session
from app.models import Products

# Настроим логгер
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def seed_data() -> None:
    async with async_session() as session:
        existing = await session.execute(select(Products))
        if existing.scalars().first():
            logger.info('Данные уже существуют.')
            return

        with open(PIONEER_PRODUCTS_JSON_PATH, encoding='utf-8') as file:
            pioneer_products = load(file)

        with open(REPEATER_PRODUCTS_JSON_PATH, encoding='utf-8') as file:
            repeater_products = load(file)

        all_products_data = pioneer_products + repeater_products
        products = [Products(**data) for data in all_products_data]

        session.add_all(products)
        await session.commit()
        logger.info('База успешно заполнена тестовыми продуктами.')


if __name__ == '__main__':
    asyncio.run(seed_data())
