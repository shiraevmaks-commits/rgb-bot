from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database.db import connect
from services.state_service import set_state
from services.ui_service import safe_send

router = Router()


def menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏰 Замок", callback_data="castle"),
                InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
            ],
            [
                InlineKeyboardButton(text="⛏ Рудник", callback_data="mine"),
                InlineKeyboardButton(text="⚔ Подземелье", callback_data="dungeon"),
            ],
        ]
    )


async def show_menu(message: Message):

    set_state(message.from_user.id, "MENU")

    db = await connect()

    cursor = await db.execute(
        "SELECT * FROM players WHERE user_id = ?",
        (message.from_user.id,)
    )

    player = await cursor.fetchone()
    await db.close()

    if not player:
        return

    # 📊 данные
    level = player["level"]
    energy = player["energy"]
    player_class = player["class"]

    gold = player["gold"]
    crystals = player["crystals"]
    blood = player["blood"]

    status = "Новичок"

    text = (
        "═══ 🏰 ЭТЕРИЯ • ГОРОД ═══\n\n"

        f"🏷 {player_class}        Статус: {status}\n"
        f"⭐ Уровень: {level}\n\n"

        f"💰 {gold} золота\n"
        f"🩸 {blood} крови\n"
        f"💎 {crystals} кристаллов\n\n"

        f"⚡ Энергия: {energy} / 55\n\n"

        "📍 Дополнительные действия:\n"
        "/help\n"
    )

    await safe_send(message, text, menu_kb())