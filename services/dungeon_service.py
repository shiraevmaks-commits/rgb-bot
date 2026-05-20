import random


# ⚔️ УРОН В БОЮ
def deal_damage(player_hp, monster):

    base_damage = random.randint(7, 12)

    battle_text = ""

    # 💥 крит игрока
    if random.randint(1, 100) <= 5:
        base_damage *= 2
        battle_text += "💥 КРИТ!\n"

    # 🛡 защита моба
    reduced_damage = max(1, base_damage - monster["def"])

    monster["hp"] -= reduced_damage
    battle_text += f"⚔️ Вы нанесли {reduced_damage} урона\n"

    # 👹 ответный удар
    if monster["hp"] > 0:

        monster_damage = max(1, monster["atk"] - 2)

        # 💥 крит моба
        if random.randint(1, 100) <= monster["crit"]:
            monster_damage *= 2
            battle_text += "💥 Крит врага!\n"

        player_hp -= monster_damage
        battle_text += f"👹 Монстр ударил на {monster_damage}"

    return player_hp, monster, battle_text


# ☠ смерть игрока
def is_dead(player_hp):
    return player_hp <= 0


# 🏆 победа над мобом
def is_win(monster):
    return monster["hp"] <= 0