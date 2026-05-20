from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.db import connect
from data.monsters import get_random_monster
from services.dungeon_service import deal_damage, is_dead, is_win
from services.reward_service import roll_rewards

router = Router()

# 💾 СТЕЙТ
current_monster = {}
player_hp = {}
player_max_hp = 100


# 🔘 КНОПКИ
dungeon_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⚔ Атаковать", callback_data="dungeon_attack"),
            InlineKeyboardButton(text="➡ Пройти", callback_data="dungeon_next")
        ],
        [
            InlineKeyboardButton(text="🏰 В город", callback_data="dungeon_exit")
        ]
    ]
)

fight_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⚔ Атаковать", callback_data="dungeon_attack"),
            InlineKeyboardButton(text="➡ Пройти", callback_data="blocked_next")
        ],
        [
            InlineKeyboardButton(text="🏰 В город", callback_data="dungeon_exit")
        ]
    ]
)


# 📍 ТЕКСТ ДАНЖА
def dungeon_text(user_id, monster):
    return (
        "═════ ⚔ Данж ═════\n\n"
        f"👹 Монстр: {monster['name']}\n\n"
        f"❤️ HP: {player_hp[user_id]}/{player_max_hp}\n\n"
        f"👹 HP врага: {monster['hp']}\n"
        f"⚔ ATK: {monster['atk']}\n"
        f"🛡 DEF: {monster['def']}\n"
        f"🎯 CRIT: {monster['crit']}%\n\n"
        "═══════════════"
    )


# 📍 ВХОД В ДАНЖ
@router.callback_query(F.data == "dungeon")
async def dungeon_start(callback: CallbackQuery):

    user_id = callback.from_user.id

    player_hp[user_id] = player_max_hp
    current_monster[user_id] = get_random_monster()

    await callback.message.edit_text(
        dungeon_text(user_id, current_monster[user_id]),
        reply_markup=dungeon_menu
    )

    await callback.answer()


# ➡ НОВЫЙ МОБ
@router.callback_query(F.data == "dungeon_next")
async def dungeon_next(callback: CallbackQuery):

    user_id = callback.from_user.id

    current_monster[user_id] = get_random_monster()

    await callback.message.edit_text(
        dungeon_text(user_id, current_monster[user_id]),
        reply_markup=dungeon_menu
    )

    await callback.answer()


# ❌ БЛОК
@router.callback_query(F.data == "blocked_next")
async def blocked_next(callback: CallbackQuery):
    await callback.answer("Сначала бой", show_alert=True)


# ⚔ АТАКА
@router.callback_query(F.data == "dungeon_attack")
async def dungeon_attack(callback: CallbackQuery):

    user_id = callback.from_user.id

    if user_id not in current_monster:
        await callback.answer("Нет монстра")
        return

    monster = current_monster[user_id]

    # ⚔ бой
    player_hp[user_id], monster, battle_text = deal_damage(
        player_hp[user_id],
        monster
    )

    # ☠ смерть
    if is_dead(player_hp[user_id]):

        current_monster.pop(user_id, None)
        player_hp[user_id] = player_max_hp

        await callback.message.edit_text(
            "☠️ Вы погибли\n\n🏰 Возвращение в город..."
        )

        await callback.answer()
        return

    # 🏆 победа
    if is_win(monster):

        gold, xp, eggs, blood = roll_rewards(monster["name"])

        db = await connect()

        await db.execute("""
            UPDATE players
            SET gold = gold + ?,
                xp = xp + ?,
                eggs = eggs + ?,
                blood = blood + ?
            WHERE user_id = ?
        """, (gold, xp, eggs, blood, user_id))

        await db.commit()
        await db.close()

        current_monster.pop(user_id, None)

        await callback.message.edit_text(
            f"🎁 Победа!\n\n{battle_text}\n\n"
            f"💰 +{gold}\n"
            f"⭐ +{xp}\n"
            f"🩸 +{blood}\n"
            f"🥚 +{eggs}",
            reply_markup=dungeon_menu
        )

        await callback.answer("Победа")
        return
# 🔄 бой продолжается
    try:
        await callback.message.edit_text(
            dungeon_text(user_id, monster) + "\n\n" + battle_text,
            reply_markup=fight_menu
        )
    except:
        await callback.message.answer(
            dungeon_text(user_id, monster) + "\n\n" + battle_text,
            reply_markup=fight_menu
        )

    await callback.answer()


# 🏰 ВЫХОД
@router.callback_query(F.data == "dungeon_exit")
async def dungeon_exit(callback: CallbackQuery):

    user_id = callback.from_user.id

    current_monster.pop(user_id, None)
    player_hp[user_id] = player_max_hp

    await callback.message.edit_text(
        "🏰 Вы вернулись в город\n/start"
    )

    await callback.answer()