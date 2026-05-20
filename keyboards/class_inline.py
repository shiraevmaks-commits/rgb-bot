from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⚔ Мечник", callback_data="class_warrior")
        ],
        [
            InlineKeyboardButton(text="🪄 Маг", callback_data="class_mage")
        ],
        [
            InlineKeyboardButton(text="🏹 Лучник", callback_data="class_archer")
        ]
    ]
)