from decimal import Decimal
from models import UserTable, Base, RefuelingTable

from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config_db import settings


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

    def add_user(self, username: str, name: str, id_telegram: int):
        with self.session_factory() as session:
            added_user = self.model(username=username, name=name, id_telegram=id_telegram)
            session.add(added_user)
            session.commit()

    def get_user(self, user_id: int):
        with self.session_factory() as session:
            query = select(self.model).filter_by(id=user_id)
            res = session.execute(query)
            return res.scalars().all()[0]

    def update_name(self, user_id: int, new_name: str):
        with self.session_factory() as session:
            query = update(self.model).filter_by(id=user_id).values(name=new_name)
            session.execute(query)
            session.commit()


class RefuelingORM(BaseOrm):
    def __init__(self):
        super().__init__()
        self.model = RefuelingTable

    def add_refueling(
            self,
            id_user: int,
            amount_gasoline: Decimal,
            mileage: Decimal,
            cost_refueling: Decimal,
            price_gasoline: Decimal
    ):
        with self.session_factory() as session:
            added_refuel = self.model(
                user_id=id_user,
                amount_gasoline=amount_gasoline,
                mileage=mileage,
                cost_refueling=cost_refueling,
                price_gasoline=price_gasoline
            )
            session.add(added_refuel)
            session.commit()

    def get_refuel(self, id_user: int):
        with self.session_factory() as session:
            query = select(self.model).where(self.model.user_id == id_user)
            res = session.execute(query)
            return res.scalars().all()[0]
