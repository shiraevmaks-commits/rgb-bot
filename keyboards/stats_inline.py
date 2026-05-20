from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


stats_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="profile"
            )
        ]
    ]
)