from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import random

from database.db import connect

router = Router()


# 🐾 КНОПКИ
pets_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🥚 Вылупить",
                callback_data="hatch_pet"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="profile"
            )
        ]
    ]
)


# 🐣 СПИСОК ПИТОМЦЕВ
pets_pool = [
    ("🐀 Крысеныш", "Обычный"),
    ("🕷 Паучок", "Обычный"),
    ("🐍 Змейка", "Редкий"),
    ("👻 Фантом", "Эпический"),
    ("💀 Костяной страж", "Легендарный")
]


# 🐾 ОКНО ПИТОМЦЕВ
@router.callback_query(F.data == "pets")
async def pets(callback: CallbackQuery):

    db = await connect()

    cursor = await db.execute("""
        SELECT eggs
        FROM players
        WHERE user_id = ?
    """, (callback.from_user.id,))

    player = await cursor.fetchone()

    await db.close()

    eggs = player["eggs"]

    text = (
        "═════ 🐾 Питомец ═════\n\n"

        "🐣 Активный питомец: Нет\n"
        "⭐ Редкость: —\n"
        "📈 Уровень: 0\n\n"

        "🗡 Бонус атаки: 0%\n"
        "🛡 Бонус защиты: 0%\n"
        "❤️ Бонус HP: 0%\n"
        "💀 Доп. жизни: 0\n\n"

        f"🥚 Яиц: {eggs}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=pets_menu
    )

    await callback.answer()


# 🥚 ВЫЛУПЛЕНИЕ
@router.callback_query(F.data == "hatch_pet")
async def hatch_pet(callback: CallbackQuery):

    db = await connect()

    cursor = await db.execute("""
        SELECT eggs
        FROM players
        WHERE user_id = ?
    """, (callback.from_user.id,))

    player = await cursor.fetchone()

    eggs = player["eggs"]

    if eggs <= 0:

        await callback.answer(
            "У вас нет яиц",
            show_alert=True
        )

        await db.close()

        return

    # 🥚 -1 ЯЙЦО
    await db.execute("""
        UPDATE players
        SET eggs = eggs - 1
        WHERE user_id = ?
    """, (callback.from_user.id,))

    await db.commit()

    await db.close()

    # 🎲 ПИТОМЕЦ
    pet_name, rarity = random.choice(pets_pool)

    await callback.message.edit_text(
        "🥚 Яйцо раскололось...\n\n"
        f"🐾 Вы получили питомца:\n\n"
        f"{pet_name}\n"
        f"⭐ Редкость: {rarity}",
        reply_markup=pets_menu
    )

    await callback.answer()


# 📩 КОМАНДА
@router.message(F.text == ".питомец")
async def pets_command(message: Message):

    db = await connect()

    cursor = await db.execute("""
        SELECT eggs
        FROM players
        WHERE user_id = ?
    """, (message.from_user.id,))

    player = await cursor.fetchone()

    await db.close()

    eggs = player["eggs"]

    text = (
        "═════ 🐾 Питомец ═════\n\n"

        "🐣 Активный питомец: Нет\n"
        "⭐ Редкость: —\n"
        "📈 Уровень: 0\n\n"

        "🗡 Бонус атаки: 0%\n"
        "🛡 Бонус защиты: 0%\n"
        "❤️ Бонус HP: 0%\n"
        "💀 Доп. жизни: 0\n\n"

        f"🥚 Яиц: {eggs}"
    )

    await message.answer(
        text,
        reply_markup=pets_menu
    )