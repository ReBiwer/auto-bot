from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy import delete
from sqlalchemy import exists
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import join
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker

from db_settings.config_db import settings
from db_settings.db_models import Base
from db_settings.db_models import Refueling
from db_settings.db_models import User
from db_settings.DTO_models import RefuelChangeDTO
from db_settings.DTO_models import RefuelGetDTO
from db_settings.DTO_models import UserChangeDTO
from db_settings.DTO_models import UserGetDTO


class BaseAppModel:
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


class UserAppModel(BaseAppModel):
    def __init__(self):
        super().__init__()
        self.model = User

    async def check_user(self, id_telegram: int) -> bool:
        async with self.async_session_factory() as session:
            check_query = select(exists().where(self.model.id_telegram == id_telegram))
            res = await session.execute(check_query)
            return res.scalar()

    async def add_user(self, user: UserChangeDTO) -> bool:
        async with self.async_session_factory() as session:
            added_user = self.model(username=user.username, name=user.name, id_telegram=user.id_telegram)
            check_user = await self.check_user(user.id_telegram)
            if not check_user:
                session.add(added_user)
                await session.commit()
            return check_user

    async def get_user(self, id_telegram: int) -> UserGetDTO | bool:
        async with self.async_session_factory() as session:
            query = select(self.model).filter_by(id_telegram=id_telegram)
            check_user = await self.check_user(id_telegram)
            if check_user:
                res = await session.execute(query)
                user = res.scalars().one()
                user_gto = UserGetDTO.model_validate(user, from_attributes=True)
                return user_gto
            return check_user

    async def update_user(self, user: UserChangeDTO) -> None:
        async with self.session_factory() as session:
            query = (
                update(self.model)
                .filter_by(id_telegram=user.id_telegram)
                .values(name=user.new_name, username=user.new_username)
            )
            await session.execute(query)
            await session.commit()

    async def delete_user(self, id_user: int) -> None:
        async with self.async_session_factory() as session:
            query = delete(self.model).filter_by(id=id_user)
            await session.execute(query)
            await session.commit()


class RefuelingAppModel(BaseAppModel):
    def __init__(self):
        super().__init__()
        self.model = Refueling

    async def add_refueling(self, refuel: RefuelChangeDTO) -> None:
        async with self.async_session_factory() as session:
            added_refuel = self.model(
                user_id=refuel.user_id,
                amount_gasoline=refuel.amount_gasoline,
                mileage=refuel.mileage,
                cost_refueling=refuel.cost_refueling,
                price_gasoline=refuel.price_gasoline,
            )
            session.add(added_refuel)
            await session.commit()

    async def get_refuels(self, id_telegram: int) -> dict[int, RefuelGetDTO]:
        async with self.async_session_factory() as session:
            query = (
                select(Refueling)
                .join(Refueling.user)
                .options(contains_eager(Refueling.user))
                .filter(User.id_telegram == id_telegram)
            )
            res = await session.execute(query)
            refuels = res.unique().scalars().all()
            refuels_dto = {row.id: RefuelGetDTO.model_validate(row, from_attributes=True) for row in refuels}
        return refuels_dto

    async def update_refuel(self, refuel: RefuelChangeDTO) -> None:
        async with self.async_session_factory() as session:
            query = (
                update(self.model)
                .filter_by(id=refuel.id)
                .values(
                    user_id=refuel.user_id,
                    amount_gasoline=refuel.amount_gasoline,
                    mileage=refuel.mileage,
                    cost_refueling=refuel.cost_refueling,
                    price_gasoline=refuel.price_gasoline,
                )
            )
            await session.execute(query)
            await session.commit()

    async def delete_refuel(self, id_refuel: int) -> None:
        async with self.async_session_factory() as session:
            query = delete(self.model).filter_by(id=id_refuel)
            await session.execute(query)
            await session.commit()
