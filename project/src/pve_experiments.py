# Import parts
import random
import numpy as np
import matplotlib.pyplot as plt

# Load modules
from unit import Unit, Player, Monster
from mab import EpsilonGreedy, UCB1, AOUCB, ThompsonSampling
from util import *

class PvE:
    def __init__(self, player_num = 20,
                        difficulty_num = 5,
                        player_health_lower = 100,
                        player_health_upper = 200,
                        monster_health_lower = 100,
                        monster_health_upper = 200):
        print("################ Init PvE system #################")
        self.player_num = player_num
        self.difficulty_num = difficulty_num # number of arms
        self.player_health_lower = player_health_lower

        self.players = []
        self.monsters = []

        # Init Players
        for i in range(player_num):
            health = random.randint(player_health_lower, player_health_upper)
            h, a, d = generate_linear_attributes(health)
            p = Player(h, a, d, f"P{i+1}")
            self.players.append(p)

        # Init Monsters
        monster_health = np.linspace(monster_health_lower, monster_health_upper, self.difficulty_num)
        for j in monster_health:
            h, a, d = generate_linear_attributes(health, interval_coef = 0.05) # More stable difficulty for experiments
            m = Monster(h, a, d, f"M{j+1}")
            self.monsters.append(m)

        # Init Bandits
        self.optimal_reward = 4
        self.bandits = {
            'epsilon_greedy': EpsilonGreedy(self.difficulty_num, player_num),
            'ucb1': UCB1(self.difficulty_num, player_num),
            'aoucb': AOUCB(self.difficulty_num, player_num),
            'thompson_sampling': ThompsonSampling(self.difficulty_num, player_num)
        }

    def calculate_reward(self, health, round, win):
        assert (win == 0) or (win == 1), f"Error {win}"
        # Rule1: win means +1, lose means 0
        # Rule2: normalized_round = round * health_lower_bound / health, cause round grows (approximately) linear with health
        # normalized reward: 0 (0-70 rounds), 1(70-150 rounds), 2(150-250 rounds), 3(250+rounds)
        n_round = 1.0 * round * self.player_health_lower / health

        round_reward = 0
        if n_round > 70 and n_round <= 150:
            round_reward = 1
        elif n_round > 150 and n_round <= 250:
            round_reward = 2
        else:
            round_reward = 3

        return win + round_reward

    def run(self, n_rounds_per_player=10000, algorithm='ucb1'):
        
        print(f"################ Running PvE system with {algorithm} #################")
        cumulative_regrets_matrix = []
        average_regrets_matrix = []

        for i, player in enumerate(self.players):
            print(f"Running Simulation for {player.name}")

            bandit = self.bandits[algorithm]
            cumulative_regret = np.zeros(n_rounds_per_player) # Record cumulative regret
            average_regret = np.zeros(n_rounds_per_player) # Record average regret 

            for round_num in range(n_rounds_per_player):
                # if (round_num + 1) % 1000 == 0:
                #     print(f"Tournament {round_num + 1}")
                selected_monster_index = bandit.select_arm(round_num)
                monster = self.monsters[selected_monster_index]

                rounds, win = battle1v1(player, monster)
                player.reset()
                monster.reset()

                reward = self.calculate_reward(player.health, rounds, win)

                regret = self.optimal_reward - reward # Regret formula
                cumulative_regret[round_num] = cumulative_regret[round_num - 1] + regret if round_num > 0 else regret
                average_regret[round_num] = cumulative_regret[round_num] / (round_num + 1.0) 

                bandit.update(selected_monster_index, reward)
            
            # After n_rounds_per_player, append result into matrix
            cumulative_regrets_matrix.append(cumulative_regret)
            average_regrets_matrix.append(average_regret)

        # Convert lists to numpy arrays for easier manipulation
        cumulative_regrets_matrix = np.array(cumulative_regrets_matrix)
        average_regrets_matrix = np.array(average_regrets_matrix)

        return cumulative_regrets_matrix, average_regrets_matrix
    
    def run_all_algorithms(self, n_rounds_per_player = 5000):
        cumulative_regret_results_mean = {}
        cumulative_regret_results_std = {}
        average_regret_results_mean = {}
        algorithms = ['epsilon_greedy', 'ucb1', 'aoucb', 'thompson_sampling']

        for algo in algorithms:
            cumulative_regrets_matrix, average_regrets_matrix = self.run(n_rounds_per_player, algo)
            cumulative_regret_results_mean[algo] = np.mean(cumulative_regrets_matrix, axis=0)
            cumulative_regret_results_std[algo] = np.std(cumulative_regrets_matrix, axis=0)
            average_regret_results_mean[algo] = np.mean(average_regrets_matrix, axis=0)

        plt.figure(figsize=(10, 6))

        for algo in algorithms:
            plt.plot(range(n_rounds_per_player), cumulative_regret_results_mean[algo], label=f'{algo.capitalize()}')
            # Plot mean with shaded area for std deviation
            plt.fill_between(range(n_rounds_per_player), 
                            cumulative_regret_results_mean[algo] - cumulative_regret_results_std[algo], 
                            cumulative_regret_results_mean[algo] + cumulative_regret_results_std[algo], 
                            alpha=0.2)

        # Labels and title
        plt.xlabel('Rounds (t)')
        plt.ylabel('cumulative Regret')
        plt.title(f'Mean cumulative regret with Error Bars(1-std)')

        plt.grid(True)
        plt.legend()
        plt.show()

        #### Plotting Average Regret
        plt.figure(figsize=(10, 6))
        for algo in algorithms:
            plt.plot(range(n_rounds_per_player), average_regret_results_mean[algo], label=f'{algo.capitalize()}')

        # Labels and title
        plt.xlabel('Rounds (t)')
        plt.ylabel('Average Regret')
        plt.title(f'Mean Average regret')

        plt.grid(True)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    pve_env = PvE(player_num=20)
    pve_env.run_all_algorithms(n_rounds_per_player=10000)