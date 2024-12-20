import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.add_refueling import add_refuel_router
from handlers.detail_refueling import detail_refueling_router
from middlewares.user import UserDBMiddleware
from middlewares.refueling import RefuelsMiddleware
from aiogram.types import BotCommand, BotCommandScopeDefault
# from work_time.time_func import send_time_msg


async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='add_refueling', description='Добавить заправку'),
                BotCommand(command='detail_refueling', description='Узнать о своих заправках'),]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_routers(
        start_router,
        add_refuel_router,
        detail_refueling_router,
    )
    dp.message.middleware(UserDBMiddleware())
    dp.callback_query.middleware(UserDBMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
