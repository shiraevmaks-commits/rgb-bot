from aiogram import Router, F
from aiogram.types import Message

from database.db import connect

router = Router()

# 🔐 АДМИНЫ
ADMIN_IDS = [5274938222]  # <-- сюда свой user_id


# 📌 ПРОВЕРКА АДМИНА
def is_admin(user_id: int):
    return user_id in ADMIN_IDS


# 🛠 /admin
@router.message(F.text == "/admin")
async def admin_panel(message: Message):

    if not is_admin(message.from_user.id):
        await message.answer("⛔ Нет доступа")
        return

    await message.answer(
        "🛠 Админка 1.0\n\n"
        "/give_gold user_id amount\n"
        "/give_xp user_id amount\n"
        "/give_eggs user_id amount\n"
        "/set_level user_id level"
    )


# 💰 ЗОЛОТО
@router.message(F.text.startswith("/give_gold"))
async def give_gold(message: Message):

    if not is_admin(message.from_user.id):
        return

    _, user_id, amount = message.text.split()

    db = await connect()

    await db.execute("""
        UPDATE players
        SET gold = gold + ?
        WHERE user_id = ?
    """, (int(amount), int(user_id)))

    await db.commit()
    await db.close()

    await message.answer("💰 Выдано золото")


# ⭐ XP
@router.message(F.text.startswith("/give_xp"))
async def give_xp(message: Message):

    if not is_admin(message.from_user.id):
        return

    _, user_id, amount = message.text.split()

    db = await connect()

    await db.execute("""
        UPDATE players
        SET xp = xp + ?
        WHERE user_id = ?
    """, (int(amount), int(user_id)))

    await db.commit()
    await db.close()

    await message.answer("⭐ Выдан опыт")


# 🥚 ЯЙЦА
@router.message(F.text.startswith("/give_eggs"))
async def give_eggs(message: Message):

    if not is_admin(message.from_user.id):
        return

    _, user_id, amount = message.text.split()

    db = await connect()

    await db.execute("""
        UPDATE players
        SET eggs = eggs + ?
        WHERE user_id = ?
    """, (int(amount), int(user_id)))

    await db.commit()
    await db.close()

    await message.answer("🥚 Выданы яйца")


# 📈 УРОВЕНЬ
@router.message(F.text.startswith("/set_level"))
async def set_level(message: Message):

    if not is_admin(message.from_user.id):
        return

    _, user_id, level = message.text.split()

    db = await connect()

    await db.execute("""
        UPDATE players
        SET level = ?
        WHERE user_id = ?
    """, (int(level), int(user_id)))

    await db.commit()
    await db.close()

    await message.answer("📈 Уровень изменён")
