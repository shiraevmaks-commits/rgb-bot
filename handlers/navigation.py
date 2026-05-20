from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.menu import show_menu
from services.state_service import get_state, set_state, clear_state

router = Router()


# 🔙 ЕДИНЫЙ BACK
@router.callback_query(F.data == "back")
async def back_router(callback: CallbackQuery):

    user_id = callback.from_user.id
    state = get_state(user_id)

    # 🏰 ОСНОВНЫЕ ЭКРАНЫ → МЕНЮ
    if state in {"MENU", "CASTLE", "PROFILE", "MINE", "PETS", "STATS"}:

        set_state(user_id, "MENU")

        await show_menu(callback)

    # ⚔ ДАНЖ → ГОРОД
    elif state == "DUNGEON":

        set_state(user_id, "MENU")
        clear_state(user_id)

        await callback.message.edit_text(
            "🏰 Вы вернулись в город\n/start"
        )

    await callback.answer()