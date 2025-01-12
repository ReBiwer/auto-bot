from decimal import Decimal
from db_handler.models import UserTable, Base, RefuelingTable

from sqlalchemy import create_engine, select, update, delete, exists
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db_handler.config_db import settings


class BaseOrm:
    def __init__(self):
        self.engine = create_engine(
            url=settings.DATABASE_URL_psycopg,
            # echo=True,
        )
        self.async_engine = create_async_engine(
            url=settings.DATABASE_URL_asyncpg,
            # echo=True
        )
        self.session_factory = sessionmaker(self.engine)
        self.async_session_factory = async_sessionmaker(self.async_engine)

    def create_table(self):
        Base.metadata.create_all(self.engine)


class UserORM(BaseOrm):
    def __init__(self):
        super().__init__()
        self.model = UserTable

    async def check_user(self, id_telegram: int) -> bool:
        async with self.async_session_factory() as session:
            check_query = select(exists().where(self.model.id_telegram == id_telegram))
            res = await session.execute(check_query)
            return res.scalar()

    async def add_user(self, username: str, name: str, id_telegram: int) -> bool:
        async with self.async_session_factory() as session:
            added_user = self.model(username=username, name=name, id_telegram=id_telegram)
            check_user = await self.check_user(id_telegram)
            if not check_user:
                session.add(added_user)
                await session.commit()
            return check_user

    async def get_user(self, id_telegram: int) -> UserTable| bool:
        async with self.async_session_factory() as session:
            query = select(self.model).filter_by(id_telegram=id_telegram)
            check_user = await self.check_user(id_telegram)
            if check_user:
                res = await session.execute(query)
                return res.scalars().one()
            return check_user

    async def update_user(self, id_telegram: int, new_name: str, new_username) -> None:
        async with self.session_factory() as session:
            query = (
                update(self.model)
                .filter_by(id_telegram=id_telegram)
                .values(name=new_name, username=new_username)
            )
            await session.execute(query)
            await session.commit()

    async def delete_user(self, id_user: int) -> None:
        async with self.async_session_factory as session:
            query = delete(self.model).filter_by(id=id_user)
            await session.execute(query)
            await session.commit()


class RefuelingORM(BaseOrm):
    def __init__(self):
        super().__init__()
        self.model = RefuelingTable

    async def add_refueling(
            self,
            id_user: int,
            amount_gasoline: str | Decimal,
            mileage: str | Decimal,
            cost_refueling: str | Decimal,
            price_gasoline: str | Decimal
    ) -> None:
        async with self.async_session_factory() as session:
            added_refuel = self.model(
                user_id=id_user,
                amount_gasoline=Decimal(amount_gasoline),
                mileage=Decimal(mileage),
                cost_refueling=Decimal(cost_refueling),
                price_gasoline=Decimal(price_gasoline),
            )
            session.add(added_refuel)
            await session.commit()

    async def get_refuels(self, id_telegram: int) -> dict[int,  RefuelingTable]:
        async with self.async_session_factory() as session:
            query = (
                select(UserTable)
                .options(selectinload(UserTable.refuelings))
                .filter_by(id_telegram=id_telegram)
            )
            res = await session.execute(query)
        refuels = res.scalars().first().refuelings
        data = {refueling.id: refueling for refueling in refuels}
        return data

    async def update_refuel(
            self,
            id_refuel: int,
            user_id: int,
            amount_gasoline: Decimal,
            mileage: Decimal,
            cost_refueling: Decimal,
            price_gasoline: Decimal
    ) -> None:
        async with self.async_session_factory as session:
            query = update(self.model).values(
                id_refuel=id_refuel,
                user_id=user_id,
                amount_gasoline=amount_gasoline,
                mileage=mileage,
                cost_refueling=cost_refueling,
                price_gasoline=price_gasoline,
            )
            await session.execute(query)
            await session.commit()

    async def delete_refuel(self, id_refuel: int) -> None:
        async with self.async_session_factory as session:
            query = delete(self.model).filter_by(id=id_refuel)
            await session.execute(query)
            await session.commit()
