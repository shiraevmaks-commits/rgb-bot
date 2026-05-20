from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🏰 Замок", callback_data="castle"),
            InlineKeyboardButton(text="👤 Профиль", callback_data="profile")
        ],
        [
            InlineKeyboardButton(text="⛏ Рудник", callback_data="mine"),
            InlineKeyboardButton(text="🐉 Подземелье", callback_data="dungeon")
        ]
    ]
)