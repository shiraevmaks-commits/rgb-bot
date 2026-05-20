from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database.db import connect
from handlers.menu import show_menu

router = Router()


@router.message(F.text == "/start")
async def start(message: Message):

    db = await connect()

    try:

        # 🔍 ИЩЕМ ИГРОКА
        cursor = await db.execute(
            "SELECT * FROM players WHERE user_id = ?",
            (message.from_user.id,)
        )

        user = await cursor.fetchone()

        # 🆕 СОЗДАНИЕ ИГРОКА
        if not user:

            await db.execute("""
                INSERT INTO players (
                    user_id,
                    class,
                    level,
                    xp,
                    gold,
                    crystals,
                    blood,
                    eggs,
                    energy
                )
                VALUES (?, '', 1, 0, 0, 0, 0, 0, 25)
            """, (message.from_user.id,))

            await db.commit()

            cursor = await db.execute(
                "SELECT * FROM players WHERE user_id = ?",
                (message.from_user.id,)
            )

            user = await cursor.fetchone()

        # ✔ КЛАСС УЖЕ ВЫБРАН
        if user["class"]:

            await show_menu(message)
            return

        # ❌ ВЫБОР КЛАССА
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔮 Маг",
                        callback_data="class_mage"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🏹 Лучник",
                        callback_data="class_archer"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🗡 Мечник",
                        callback_data="class_swordsman"
                    )
                ]
            ]
        )

        await message.answer(
            "🏰 Добро пожаловать в Этерию...\n\n"
            "Выбери класс героя:",
            reply_markup=kb
        )

    finally:

        await db.close()