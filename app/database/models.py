import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, String, BigInteger, DateTime, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import DB_URL

engine = create_async_engine(url=DB_URL,
                             echo=True)

async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    trial_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    vpns: Mapped[list['UserVPN']] = relationship(back_populates="user")


class VPNCategory(Base):
    __tablename__ = 'vpn_categories'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(25),
                                      unique=True,
                                      nullable=False)
    vpns: Mapped[list['VPN']] = relationship(back_populates="category")


class VPN(Base):
    __tablename__ = 'vpns'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(125),
                                      nullable=False)
    price: Mapped[int] = mapped_column(Integer)
    max_conn: Mapped[int] = mapped_column(Integer)
    current_conn: Mapped[int] = mapped_column(Integer)
    server_id: Mapped[str] = mapped_column(String(225))
    server_hash: Mapped[str] = mapped_column(String(225))
    category_id: Mapped[int] = mapped_column(ForeignKey('vpn_categories.id'))
    category: Mapped['VPNCategory'] = relationship(back_populates="vpns")
    users: Mapped[list['UserVPN']] = relationship(back_populates="vpn")


class UserVPN(Base):
    __tablename__ = 'user_vpns'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    vpn_id: Mapped[int] = mapped_column(ForeignKey('vpns.id'))
    until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    user: Mapped['User'] = relationship(back_populates="vpns")
    vpn: Mapped['VPN'] = relationship(back_populates="users")


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
