from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.db import connect
from handlers.menu import show_menu

router = Router()


@router.callback_query(F.data.startswith("class_"))
async def choose_class(callback: CallbackQuery):

    class_map = {
        "class_mage": "Маг",
        "class_archer": "Лучник",
        "class_swordsman": "Мечник"
    }

    chosen = class_map.get(callback.data)

    if not chosen:
        await callback.answer("Ошибка выбора")
        return

    db = await connect()

    try:

        # 🆕 СОЗДАНИЕ ИГРОКА
        await db.execute(
            "INSERT OR IGNORE INTO players (user_id) VALUES (?)",
            (callback.from_user.id,)
        )

        # 💾 СОХРАНЕНИЕ КЛАССА
        await db.execute(
            "UPDATE players SET class = ? WHERE user_id = ?",
            (chosen, callback.from_user.id)
        )

        await db.commit()

    finally:

        await db.close()

    # 🔔 УВЕДОМЛЕНИЕ
    await callback.answer(
        f"Вы выбрали класс: {chosen}"
    )

    # 🗑 УДАЛЯЕМ ЭКРАН ВЫБОРА
    await callback.message.delete()

    # 🏰 ОТКРЫВАЕМ МЕНЮ
    await show_menu(callback)