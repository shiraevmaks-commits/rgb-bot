import random


def roll_rewards(monster_name):

    gold = random.randint(8, 25)
    xp = random.randint(5, 10)

    eggs = 0
    blood = 0

    if monster_name == "Дух":
        blood = 1

    elif monster_name == "Скелет":
        blood = 1
        if random.randint(1, 100) <= 5:
            eggs = 1

    elif monster_name == "Сундук":
        blood = 3
        if random.randint(1, 100) <= 8:
            eggs = 1

    return gold, xp, eggs, blood