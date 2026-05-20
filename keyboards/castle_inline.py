from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


castle_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🏛 Комнаты",
                callback_data="rooms"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬆ Улучшить замок",
                callback_data="upgrade_castle"
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