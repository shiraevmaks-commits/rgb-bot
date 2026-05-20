user_state = {}


# 🧠 УСТАНОВКА STATE
def set_state(user_id: int, state: str):

    if not isinstance(state, str):
        return

    user_state[user_id] = state


# 📍 ПОЛУЧЕНИЕ STATE
def get_state(user_id: int):

    return user_state.get(user_id, "MENU")


# 🗑 ОЧИСТКА STATE
def clear_state(user_id: int):

    user_state.pop(user_id, None)