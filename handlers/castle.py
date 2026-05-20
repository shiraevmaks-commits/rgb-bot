from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.state_service import set_state

router = Router()


# 🏰 ОСНОВНОЕ МЕНЮ ЗАМКА
castle_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⬆️ Улучшить замок",
                callback_data="upgrade_castle"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="back"
            )
        ]
    ]
)


# 🏰 ЭКРАН ЗАМКА
@router.callback_query(F.data == "castle")
async def castle(callback: CallbackQuery):

    set_state(callback.from_user.id, "CASTLE")

    text = (
        "═════ 🏰 Замок • 1 ур. ═════\n\n"
        "1️⃣ 🌾 Поля • 1 ур.\n\n"
        "2️⃣ ⛓ Железный рудник • 🔒(2)\n\n"
        "3️⃣ ⚒ Кузница • 🔒(7)\n\n"
        "4️⃣ 💰 Золотой рудник • 🔒(12)\n\n"
        "5️⃣ 👑 Комната лидеров • 🔒(19)\n\n"
        "6️⃣ 🌳 Царский сад • 🔒(30)\n\n"
        "7️⃣ 🏛 Тронный зал • 🔒(40)\n\n"
        "⛓ Железо: 0\n"
        "🪵 Дерево: 0\n"
        "🪨 Камень: 0\n\n"
        "❔ Если нужна помощь — /help"
    )

    await callback.message.edit_text(
        text,
        reply_markup=castle_menu
    )

    await callback.answer()


# ⬆️ УЛУЧШЕНИЕ ЗАМКА
@router.callback_query(F.data == "upgrade_castle")
async def upgrade_castle(callback: CallbackQuery):

    set_state(callback.from_user.id, "CASTLE")

    upgrade_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬆️ Подтвердить улучшение",
                    callback_data="castle_upgrade_confirm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="back"
                )
            ]
        ]
    )

    text = (
        "🏰 Улучшение замка\n\n"
        "Текущий уровень: 1\n"
        "Следующий уровень: 2\n\n"
        "Стоимость:\n\n"
        "🪵 Дерево: 100\n"
        "🪨 Камень: 50\n"
        "⛓ Железо: 25\n"
        "💰 Золото: 250\n\n"
        "════════════════\n\n"
        "После улучшения:\n"
        "🔓 Новые комнаты\n"
        "⬆️ Сила замка\n"
        "💰 Доход комнат"
    )

    await callback.message.edit_text(
        text,
        reply_markup=upgrade_menu
    )

    await callback.answer()


# 💬 КОМАНДА .замок
@router.message(F.text == ".замок")
async def castle_command(message: Message):

    set_state(message.from_user.id, "CASTLE")

    text = (
        "═════ 🏰 Замок • 1 ур. ═════\n\n"
        "1️⃣ 🌾 Поля • 1 ур.\n\n"
        "2️⃣ ⛓ Железный рудник • 🔒(2)\n\n"
        "3️⃣ ⚒ Кузница • 🔒(7)\n\n"
        "4️⃣ 💰 Золотой рудник • 🔒(12)\n\n"
        "5️⃣ 👑 Комната лидеров • 🔒(19)\n\n"
        "6️⃣ 🌳 Царский сад • 🔒(30)\n\n"
        "7️⃣ 🏛 Тронный зал • 🔒(40)\n\n"
        "⛓ Железо: 0\n"
        "🪵 Дерево: 0\n"
        "🪨 Камень: 0\n\n"
        "❔ Если нужна помощь — /help"
    )

    await message.answer(
        text,
        reply_markup=castle_menu
    )