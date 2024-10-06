from unit import Unit, Player, Monster
from util import *

def test_attack():
    h, a, d = generate_linear_attributes(health=50)
    player1 = Player(h, a, d, "P1")

    h, a, d = generate_linear_attributes(health=10000)
    monster1 = Monster(h, a, d, "M1")

    print("################Init#################")
    player1.print_status()
    player1.print_attribute()
    monster1.print_status()
    monster1.print_attribute()

    print("################Battle#################")
    battle1v1(player1, monster1)

def test_result():
    h, a, d = generate_linear_attributes(health=10)
    player1 = Player(h, a, d, "P1")

    h, a, d = generate_linear_attributes(health=50)
    monster1 = Monster(h, a, d, "M1")

    round, result = battle1v1(player1, monster1)
    print("################RESULT#################")
    print("Round: ", round, "Result: ", result)

def test_multi_battles(repeat = 100):
    h, a, d = generate_linear_attributes(health=50)
    player1 = Player(h, a, d, "P1")

    h, a, d = generate_linear_attributes(health=50)
    monster1 = Monster(h, a, d, "M1")

    print("################INIT#################")
    print(f"[ATTRIBUTE] Name: {player1.name}, Health: {player1.health}, Attack: {player1.attack}, Defense: {player1.attack}")
    print(f"[ATTRIBUTE] Name: {monster1.name}, Health: {monster1.health}, Attack: {monster1.attack}, Defense: {monster1.attack}")

    print("################Battle#################")
    rounds = []
    results = []
    for i in range(repeat):
        print(f"Experiment {i}")
        round, result = battle1v1(player1, monster1)
        rounds.append(round)
        results.append(result)

        player1.reset()
        monster1.reset()


    
    avg_round = np.average(rounds)
    
    results_p_win = np.count_nonzero(results)
    results_m_win = repeat - results_p_win
    print("################RESULT#################")
    print("Round: ", avg_round, "Result: Player win: ", results_p_win, " Monster win: ", results_m_win)

def test_different_init(repeat = 100):
    rounds = []
    results = []
    for i in range(repeat):
        h, a, d = generate_linear_attributes(linear_coef=10.0, health=100)
        player1 = Player(h, a, d, "P1")

        h, a, d = generate_linear_attributes(linear_coef=10.0, health=105, interval_coef=0.05)
        monster1 = Monster(h, a, d, "M1")

        print("################INIT#################")
        print(f"[ATTRIBUTE] Name: {player1.name}, Health: {player1.health}, Attack: {player1.attack}, Defense: {player1.attack}")
        print(f"[ATTRIBUTE] Name: {monster1.name}, Health: {monster1.health}, Attack: {monster1.attack}, Defense: {monster1.attack}")

        print("################Battle#################")
        

        round, result = battle1v1(player1, monster1)
        rounds.append(round)
        results.append(result)
    
    avg_round = np.average(rounds)
    
    results_p_win = np.count_nonzero(results)
    results_m_win = repeat - results_p_win
    print("################RESULT#################")
    print("Round: ", avg_round, "Result: Player win: ", results_p_win, " Monster win: ", results_m_win)


if __name__ == "__main__":
    # test_attack()
    # test_result()
    # test_multi_battles()
    test_different_init()
        