import aiosqlite
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from database.db import DB_NAME
from handlers.player_stats import CLASS_STATS
from keyboards.profile_inline import profile_menu

router = Router()


def build_text(class_name):

    base = CLASS_STATS.get(class_name, {
        "hp": 100,
        "atk": 10,
        "def": 5,
        "crit": 1,
        "mana": 0
    })

    return (
        "═════ 📊 Статы ═════\n\n"
        f"❤️ HP: {base['hp']}\n"
        f"⚔️ Атака: {base['atk']}\n"
        f"🛡 Защита: {base['def']}\n"
        f"🎯 Крит шанс: {base['crit']}%\n"
        f"🔷 Мана: {base['mana']}\n"
    )


@router.callback_query(F.data == "stats")
async def stats(callback: CallbackQuery):

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT class FROM players WHERE user_id = ?",
            (callback.from_user.id,)
        )
        data = await cursor.fetchone()

    class_name = data[0] if data else None

    await callback.message.edit_text(
        build_text(class_name),
        reply_markup=profile_menu
    )

    await callback.answer()


@router.message(F.text == ".статы")
async def stats_command(message: Message):

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT class FROM players WHERE user_id = ?",
            (message.from_user.id,)
        )
        data = await cursor.fetchone()

    class_name = data[0] if data else None

    await message.answer(
        build_text(class_name),
        reply_markup=profile_menu
    )