import asyncio
import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import select, Column, BigInteger, String
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from settings import dbstng

load_dotenv()
Base = declarative_base()


class AsyncDBSession:
    name_admin_db: str = dbstng.db.db_user  # Имя админа
    password_db: str = dbstng.db.db_pass
    ip_db: str = dbstng.db.db_host
    port_db: str = dbstng.db.db_port
    name_db: str = dbstng.db.db_name
    connect_db: str = f"{name_admin_db}:{password_db}@{ip_db}:{port_db}/{name_db}"

    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        print(self._session)
        return getattr(self._session, name)

    async def init(self):
        self._engine = create_async_engine(f"postgresql+asyncpg://{self.connect_db}", echo=True)
        self._session = async_sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


async_db_session = AsyncDBSession()
asyncio.run(async_db_session.init())


class MethodClassAll:
    @classmethod
    async def create(cls, acc) -> None:
        async_db_session.add(acc)
        await async_db_session.commit()


class MethodClassUser(MethodClassAll):
    @classmethod
    async def get_user(cls, tg_id: int):
        query = select(cls).where(cls.tg_id == tg_id)
        res = await async_db_session.execute(query)
        try:
            (res,) = res.one()
        except NoResultFound:
            res = None
        return res


class User(Base, MethodClassUser):
    __tablename__ = "user_profile"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    login = Column(String)
    password = Column(String)
    tg_id = Column(BigInteger)

    def __init__(self, login: str, password: str, tg_id: int):
        self.login = login
        self.password = password
        self.tg_id = tg_id

    def __repr__(self):
        return f"ID: {self.id}, Login: {self.login}"


class MethodClassCounter:

    @classmethod
    async def plus_count(cls, user_id: int):
        query = (sqlalchemy.update(cls)
                 .where(cls.user_id == user_id)
                 .values({cls.count: cls.count + 1})
                 .execution_options(synchronize_session="fetch")
                 )
        print(query.values)
        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def create(cls, acc) -> None:
        async_db_session.add(acc)
        await async_db_session.commit()

    @classmethod
    async def get_user(cls, user_id: int):
        query = select(cls).where(cls.user_id == user_id)
        res = await async_db_session.execute(query)
        try:
            (res,) = res.one()
        except NoResultFound:
            res = None
        return res


class UserCounter(Base, MethodClassCounter):
    __tablename__ = "user_counter"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    count = Column(BigInteger, default=1)

    def __init__(self, user_id: int):
        self.user_id = user_id
