import time

from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy.sql import text

from core.config import settings
from core.models.base import Base
from core.models.files_model import Files
from core.models.user_model import Users

async_engine = create_async_engine(
    settings.DATABASE_URL,
    # f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo=True,
)
async_session = async_sessionmaker(async_engine)


async def create_model():
    async with async_engine.begin() as conn:
        # В тестовом режиме чистим базу данных каждый раз перед запустом программы
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def ping_database():
    async with async_session() as session:
        try:
            start_time = time.time()
            await session.execute(text("SELECT 1"))
            end_time = time.time()
            return end_time - start_time
        except DBAPIError:
            return None


async def find_user_by_name(name: str) -> Users:
    async with async_session() as session:
        query = select(Users).where(Users.name == name)
        user = await session.scalar(query)
        return user


async def create_user(name, hash_password) -> Users:
    async with async_session() as session:
        user = Users(name=name, hash_password=hash_password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def add_file(name: str, size: int, user: Users):
    async with async_session() as session:
        new_file = Files(
            name=name,
            size=size,
            user=user,
            user_id=user.id,
        )
        session.add(new_file)
        await session.commit()
        return new_file


async def get_all_user_file(user: Users) -> list:
    async with async_session() as session:
        query = select(Files).where(Files.user == user)
        result = await session.execute(query)
        files = result.scalars().all()
        return files


async def find_file_by_name(user: int, name: str) -> Files:
    async with async_session() as session:
        query = select(Files).where(Files.user_id == user, Files.name == name)
        file = await session.scalar(query)
        if file:
            return file
        return None


async def find_and_delete_file(user: int, name: str) -> None:
    async with async_session() as session:
        query = select(Files).where(Files.user_id == user, Files.name == name)
        file = await session.scalar(query)
        print(file)
        await session.delete(file)
        await session.commit()
        return None


# async def get_file(s_data: str) -> Files:
#     async with async_session() as session:
#         if s_data.isdigit():
#             query = select(Files).where(Files.id == int(s_data))
#         else:
#             query = select(Files).where(Files.path == s_data)
#         file = await session.execute(query)
#         return file.scalar()