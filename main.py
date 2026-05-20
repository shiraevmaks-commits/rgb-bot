import asyncio

from aiogram import Bot, Dispatcher

from config.settings import BOT_TOKEN
from database.db import init_db

# 🧩 handlers
from handlers.start import router as start_router
from handlers.profile import router as profile_router
from handlers.stats import router as stats_router
from handlers.pets import router as pets_router
from handlers.mine import router as mine_router
from handlers.castle import router as castle_router
from handlers.class_select import router as class_router
from handlers.navigation import router as nav_router
from handlers.dungeon import router as dungeon_router
from handlers.admin import router as admin_router   # 🛠 АДМИНКА

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():

    # 🧠 БД
    await init_db()

    # 🔌 РОУТЕРЫ
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(stats_router)
    dp.include_router(pets_router)
    dp.include_router(mine_router)
    dp.include_router(castle_router)
    dp.include_router(class_router)
    dp.include_router(dungeon_router)

    # 🛠 АДМИНКА (обязательно отдельно)
    dp.include_router(admin_router)

    # 🔙 НАВИГАЦИЯ
    dp.include_router(nav_router)

    # 🚀 СТАРТ
    print("🤖 Бот запущен...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())