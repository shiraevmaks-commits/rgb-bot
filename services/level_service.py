def add_xp(xp, xp_gain):
    return xp + xp_gain


def level_up_logic(xp, level):
    need_xp = level * level * 69

    if xp >= need_xp:
        xp -= need_xp
        level += 1

    return xp, level, need_xp