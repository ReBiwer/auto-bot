import asyncio

from aiogram.types import BotCommand
from aiogram.types import BotCommandScopeDefault

from create_bot import bot
from create_bot import dp
from create_bot import scheduler
from handlers.add_refueling import add_refuel_router
from handlers.change_refueling import change_refueling_router
from handlers.delete_refueling import delete_refueling_router
from handlers.detail_refueling import detail_refueling_router
from handlers.start import start_router

# from work_time.time_func import send_time_msg


async def set_commands():
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="add_refueling", description="Добавить заправку"),
        BotCommand(command="change_refueling", description="Изменить заправку"),
        BotCommand(command="delete_refueling", description="Удалить заправку"),
        BotCommand(command="detail_refueling", description="Узнать о своих заправках"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_routers(
        start_router,
        add_refuel_router,
        detail_refueling_router,
        change_refueling_router,
        delete_refueling_router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
