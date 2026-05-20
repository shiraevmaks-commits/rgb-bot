from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.db import connect
from services.state_service import set_state

router = Router()


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):

    set_state(callback.from_user.id, "PROFILE")

    db = await connect()

    cursor = await db.execute(
        "SELECT * FROM players WHERE user_id = ?",
        (callback.from_user.id,)
    )

    player = await cursor.fetchone()
    await db.close()

    if not player:
        await callback.answer("Игрок не найден")
        return

    level = player["level"]
    xp = player["xp"]
    energy = player["energy"]
    player_class = player["class"]

    # ⚔️ временные статы (потом подключим систему)
    hp = 120
    atk = 20
    defense = 10
    crit = 8

    text = (
        "═════ 👤 ПЕРСОНАЖ ═════\n"
        f"⭐ Уровень: {level}        📈 {xp} / 100 XP\n"
        f"🏷 Класс: {player_class}\n\n"

        f"⚔️ Здоровье: {hp}\n"
        f"💥 Атака: {atk}\n"
        f"🛡 Защита: {defense}\n"
        f"🎯 Крит: {crit}%\n\n"

        f"⚡ Энергия: {energy} / 55\n\n"

        "🐾 Питомец: Нет\n"
        "🌍 Статус: Новичок в Этерии"
    )

    await callback.message.edit_text(text)
    await callback.answer()