import asyncio
from app.db_handler.orm import UserORM, RefuelingORM
from app.db_handler.models import UserTable, RefuelingTable
from decimal import Decimal

if __name__ == '__main__':
    tg_id_user = 437878719
    # user_db = UserORM()
    # user: UserTable = asyncio.run(user_db.get_user(tg_id_user))
    # print(user)

    refuel_db = RefuelingORM()
    # refuel_db.create_table()

    # asyncio.run(refuel_db.add_refueling(
    #     id_user=1,
    #     amount_gasoline=Decimal('45.56'),
    #     mileage=Decimal('10078.89'),
    #     cost_refueling=Decimal('2456.77'),
    #     price_gasoline=Decimal('52.89')
    # ))
    refuels: list[RefuelingTable] = asyncio.run(refuel_db.get_refuels(tg_id_user))
    print(refuels[0].cost_refueling)
