from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


mine_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⛏ Копать",
                callback_data="mine_dig"
            )
        ],
        [
            InlineKeyboardButton(
                text="📦 Инвентарь",
                callback_data="mine_inv"
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back"
            )
        ]
    ]
)