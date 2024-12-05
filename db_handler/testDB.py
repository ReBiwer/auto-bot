from orm import UserORM, RefuelingORM
from models import UserTable
from decimal import Decimal

if __name__ == '__main__':
    user_db = UserORM()
    user: UserTable = user_db.get_user(1111)
    print(type(user))
    print(user.username)
    # refuel_db = RefuelingORM()
    # refuel_db.create_table()
    # refuel_db.add_refueling(
    #     id_user=1,
    #     amount_gasoline=Decimal('45.56'),
    #     mileage=Decimal('10078.89'),
    #     cost_refueling=Decimal('2456.77'),
    #     price_gasoline=Decimal('52.89')
    # )
    # print(refuel_db.get_refuel(1))
