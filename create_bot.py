import os
import logging
import dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

dotenv.load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_NUM_DB = os.environ.get("REDIS_NUM_DB")

redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_NUM_DB}"

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
admins = [int(admin_id) for admin_id in os.environ.get("ADMINS").split(",")]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(
    token=os.environ.get("BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
storage = RedisStorage.from_url(redis_url)
dp = Dispatcher(storage=storage)
