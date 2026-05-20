from aiogram.types import Message, CallbackQuery


async def safe_send(event, text: str, keyboard=None):

    # 🔘 CALLBACK
    if isinstance(event, CallbackQuery):

        try:

            return await event.message.edit_text(
                text,
                reply_markup=keyboard
            )

        except:

            return await event.message.answer(
                text,
                reply_markup=keyboard
            )

    # 💬 MESSAGE
    if isinstance(event, Message):

        return await event.answer(
            text,
            reply_markup=keyboard
        )