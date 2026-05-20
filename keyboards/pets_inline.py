from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


pets_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🥚 Яйца",
                callback_data="eggs"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬆ Улучшить",
                callback_data="upgrade_pet"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔥 Эволюция",
                callback_data="evolution"
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="profile"
            )
        ]
    ]
)