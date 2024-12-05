import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.refueling import refuel_router
from middlewares.user import MyMiddleware
from aiogram.types import BotCommand, BotCommandScopeDefault
# from work_time.time_func import send_time_msg


async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='refueling_add', description='Добавить заправку')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_routers(
        start_router,
        refuel_router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
