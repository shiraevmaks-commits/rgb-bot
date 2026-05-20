from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.db import connect
from services.state_service import set_state
import random
import asyncio

router = Router()


# 🧠 антиспам (1 сек)
cooldown = {}


# ⛏ МЕНЮ
mine_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🪵 Дерево", callback_data="mine_wood"),
            InlineKeyboardButton(text="🪨 Камень", callback_data="mine_stone"),
        ],
        [
            InlineKeyboardButton(text="🔙 Выйти", callback_data="back")
        ]
    ]
)


# ⛏ РУДНИК
@router.callback_query(F.data == "mine")
async def mine(callback: CallbackQuery):

    set_state(callback.from_user.id, "MINE")

    text = (
        "⛏ Рудник\n\n"
        "🪵 Дерево — обычный ресурс\n"
        "🪨 Камень — шанс на железо\n\n"
        "⚡ 1 добыча = -1 энергия"
    )

    await callback.message.edit_text(text, reply_markup=mine_menu)
    await callback.answer()


# 🧠 ПРОВЕРКА ИГРОКА
async def get_player(db, user_id):
    cursor = await db.execute(
        "SELECT energy FROM players WHERE user_id = ?",
        (user_id,)
    )
    return await cursor.fetchone()


# 🪵 ДЕРЕВО
@router.callback_query(F.data == "mine_wood")
async def mine_wood(callback: CallbackQuery):

    user_id = callback.from_user.id

    # ⛔ антиспам
    if cooldown.get(user_id):
        await callback.answer("⏳ Подожди", show_alert=True)
        return

    cooldown[user_id] = True
    asyncio.create_task(reset_cd(user_id))

    db = await connect()

    player = await get_player(db, user_id)

    if not player:
        await callback.answer("Сначала /start", show_alert=True)
        await db.close()
        return

    if player["energy"] <= 0:
        await callback.answer("⚡ Нет энергии", show_alert=True)
        await db.close()
        return

    wood = random.randint(1, 3)

    await db.execute("""
        UPDATE players
        SET wood = wood + ?,
            energy = energy - 1
        WHERE user_id = ?
    """, (wood, user_id))

    await db.commit()
    await db.close()

    await callback.message.edit_text(
        f"🪵 +{wood} дерева\n⚡ -1 энергия",
        reply_markup=mine_menu
    )

    await callback.answer()


# 🪨 КАМЕНЬ + ЖЕЛЕЗО + КРИТ
@router.callback_query(F.data == "mine_stone")
async def mine_stone(callback: CallbackQuery):

    user_id = callback.from_user.id

    # ⛔ антиспам
    if cooldown.get(user_id):
        await callback.answer("⏳ Подожди", show_alert=True)
        return

    cooldown[user_id] = True
    asyncio.create_task(reset_cd(user_id))

    db = await connect()

    player = await get_player(db, user_id)

    if not player:
        await callback.answer("Сначала /start", show_alert=True)
        await db.close()
        return

    if player["energy"] <= 0:
        await callback.answer("⚡ Нет энергии", show_alert=True)
        await db.close()
        return

    # 🪨 базовый камень
    stone = random.randint(1, 2)

    # 💥 крит добыча (x2)
    crit_text = ""
    if random.randint(1, 100) <= 10:
        stone *= 2
        crit_text = "💥 КРИТ!\n"

    # ⛓ железо (редкое)
    iron = 0
    if random.randint(1, 100) <= 20:
        iron = 1

    await db.execute("""
        UPDATE players
        SET stone = stone + ?,
            iron = iron + ?,
            energy = energy - 1
        WHERE user_id = ?
    """, (stone, iron, user_id))

    await db.commit()
    await db.close()

    text = crit_text + f"🪨 +{stone} камня"

    if iron:
        text += f"\n⛓ +{iron} железа"

    text += "\n⚡ -1 энергия"

    await callback.message.edit_text(text, reply_markup=mine_menu)
    await callback.answer()


# 🧊 антиспам сброс
async def reset_cd(user_id):
    await asyncio.sleep(1)
    cooldown.pop(user_id, None)