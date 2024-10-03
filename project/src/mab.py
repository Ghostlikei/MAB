# File: mab.py
# A basic implementation for e-greedy, UCB1, AOUCB and Thompson Sampling algorithms
import numpy as np
import random

# Abstract class for context free multi armed bandits
class MAB:
    def __init__(self, k, n):
        self.k = k
        self.n = n

        self.arm_means = np.zeros(k)
        self.arm_counts = np.zeros(k)

    def regret_function(self, optimal_reward, reward):
        return optimal_reward - reward

    def select_arm(self, t):
        raise NotImplementedError

    def update(self, arm, reward):
        raise NotImplementedError

    def run(self, rewards, n):
        # Actually, we do not need this function for this Monster game environment
        raise NotImplementedError

class EpsilonGreedy(MAB):
    def __init__(self, k, n, epsilon=0.1):
        super().__init__(k, n)
        self.epsilon = epsilon
    
    def select_arm(self, t):
        # Epsilon-Greedy Strategy: Explore with probability epsilon
        if random.random() < self.epsilon:
            return random.randint(0, self.k - 1)
        else:
            return np.argmax(self.arm_means)
    
    def update(self, arm, reward):
        # Update the mean estimate and arm count for the selected arm
        self.arm_counts[arm] += 1
        self.arm_means[arm] += (reward - self.arm_means[arm]) / self.arm_counts[arm]

class UCB1(MAB):
    def __init__(self, k, n, B=2):
        super().__init__(k, n)
        self.B = B  # Exploration parameter
    
    def select_arm(self, t):
        ucb_values = np.zeros(self.k)
        for i in range(self.k):
            if self.arm_counts[i] == 0:
                return i  # Always explore arms that haven't been pulled yet
            # UCB1 calculation
            ucb_values[i] = self.arm_means[i] + self.B * np.sqrt(2 * np.log(t + 1) / self.arm_counts[i])
        return np.argmax(ucb_values)
    
    def update(self, arm, reward):
        self.arm_counts[arm] += 1
        self.arm_means[arm] += (reward - self.arm_means[arm]) / self.arm_counts[arm]

class AOUCB(MAB):
    def __init__(self, k, n, B=2):
        super().__init__(k, n)
        self.B = B
    
    def select_arm(self, t):
        ucb_values = np.zeros(self.k)
        for i in range(self.k):
            if self.arm_counts[i] == 0:
                return i  # Always explore arms that haven't been pulled yet
            # AOUCB calculation (f_t is an increasing function of time)
            f_t = 1 + t * (np.log(t + 1))**2
            ucb_values[i] = self.arm_means[i] + self.B * np.sqrt(2 * np.log(f_t) / self.arm_counts[i])
        return np.argmax(ucb_values)
    
    def update(self, arm, reward):
        self.arm_counts[arm] += 1
        self.arm_means[arm] += (reward - self.arm_means[arm]) / self.arm_counts[arm]

class ThompsonSampling(MAB):
    def __init__(self, k, n):
        super().__init__(k, n)
        self.successes = np.ones(k)  # Initialize with Beta(1,1)
        self.failures = np.ones(k)  # Initialize with Beta(1,1)
    
    def select_arm(self, t):
        sampled_values = [np.random.beta(self.successes[i], self.failures[i]) for i in range(self.k)]
        return np.argmax(sampled_values)
    
    def update(self, arm, reward):
        # Assume reward is 1 for success and 0 for failure (Bernoulli bandit)
        if reward > 0:
            self.successes[arm] += 1
        else:
            self.failures[arm] += 1
