import numpy as np

def calculate_damage(attack, defense):
    if defense >= attack:
        return 0.1 + np.random.uniform(-0.05, 0.05)
    damage = np.log(1 + attack - defense) + np.random.uniform(-0.05, 0.05)
    return damage

def generate_random_attributes(
    min_health=100,
    max_health=500,
    min_attack=1,
    max_attack=10,
    min_defense=1,
    max_defense=10
):
    health = np.random.uniform(min_health, max_health)
    attack = np.random.uniform(min_attack, max_attack)
    defense = np.random.uniform(min_defense, max_defense)
    return health, attack, defense

def generate_linear_attributes(
    linear_coef=10.0,
    health=100.0,
    interval_coef=0.2,
):
    mean = health / linear_coef
    attack = mean + np.random.uniform(-interval_coef * mean, interval_coef * mean)
    defense = mean + np.random.uniform(-interval_coef * mean, interval_coef * mean)
    return health, attack, defense

def generate_unbalanced_attributes(
    linear_coef=10.0,
    health=100.0,
    interval_coef=0.5,
    atk_coef = 2,
    def_coef = 0.5
):
    mean = health / linear_coef
    attack = atk_coef * (mean + np.random.uniform(-interval_coef * mean, interval_coef * mean))
    defense = def_coef * (mean + np.random.uniform(-interval_coef * mean, interval_coef * mean))
    return health, attack, defense

def battle1v1(player, monster):
    """
    Return: survive_round, status(1: player wins, 0: monster wins)
    """
    while player.alive() and monster.alive():
        # print(f"---Round {player.survive_rounds} ---")
        p_status = player.attack_one(monster)
        if p_status == -2:
            # print("Target was killed")
            return player.survive_rounds, 1
        elif p_status == -1:
            # print("Killed monster 1")
            player.end_round()
            return player.survive_rounds, 1
        else:
            # print(f"[DEBUG] Damage from {player.name}: ", p_status)
            m_status = monster.attack_one(player)

            if m_status == -2:
                # print("Player was killed!: -2")
                return player.survive_rounds, 0
            elif m_status == -1:
                # print("Player was killed!: -1")
                monster.end_round()
                return player.survive_rounds, 0
            else:
                # print(f"[DEBUG] Damage from {monster.name}: ", m_status)
                player.end_round()
                monster.end_round()

    raise AttributeError("Should not reach here")
    return 0, -3

if __name__ == "__main__":
    print("Testing random attributes")
    for i in range(10):
        h, a, d = generate_random_attributes()
        print(f"Health: {h}, Attack: {a}, Defense: {d}")

    print("Testing linear attributes")
    for i in range(10):
        h, a, d = generate_linear_attributes()
        print(f"Health: {h}, Attack: {a}, Defense: {d}")








