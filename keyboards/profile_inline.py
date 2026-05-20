from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


profile_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Статы", callback_data="stats"),
            InlineKeyboardButton(text="🐾 Питомец", callback_data="pets")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back")
        ]
    ]
)