from app.database.models import async_session
from app.database.models import User, Category, Item, Novelty, Item1, Manga, Item2
from sqlalchemy import select


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))


async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))


async def get_novelties():
    async with async_session() as session:
        return await session.scalars(select(Novelty))


async def get_novelty_item1(novelty_id):
    async with async_session() as session:
        return await session.scalars(select(Item1).where(Item1.novelty == novelty_id))


async def get_item1(item1_id):
    async with async_session() as session:
        return await session.scalar(select(Item1).where(Item1.id == item1_id))


async def get_mangs():
    async with async_session() as session:
        return await session.scalars(select(Manga))


async def get_manga_item2(manga_id):
    async with async_session() as session:
        return await session.scalars(select(Item2).where(Item2.manga == manga_id))


async def get_item2(item2_id):
    async with async_session() as session:
        return await session.scalar(select(Item2).where(Item2.id == item2_id))
