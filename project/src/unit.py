# Import parts
from util import calculate_damage

class Unit():
    def __init__(self, health, attack, defense, name):
        self.full_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.name = name

        self.is_alive = True
        self.survive_rounds = 0

    def attack_one(self, target):
        """
        Params:
            target: Unit
        Returns:
            damage: float, -1 means dead, -2 means error
        """
        if not target.alive():
            print("Target is dead")
            return -2
        
        damage = calculate_damage(self.attack, target.defense)
        if damage >= target.health:
            target.health = 0
            target.is_alive = False
            return -1
        else:
            target.health -= damage
        return damage
    
    def end_round(self):
        if self.is_alive:
            self.survive_rounds += 1
        else:
            return

    def reset(self):
        self.health = self.full_health
        self.is_alive = True
        self.survive_rounds = 0

    def alive(self):
        return self.is_alive

    def print_status(self):
        print("[STATUS]Name: ", self.name, 
                "Alive: ", self.is_alive, 
                "Survice Round: ", self.survive_rounds,
                "Health Remaining: ", self.health)
    
    def print_attribute(self):
        print("[ATTRIBUTE]Name: ", self.name, 
                "Health", self.health, 
                "Attack", self.attack, 
                "Defence", self.defense)

class Player(Unit):
    def __init__(self, health, attack, defense, name, attack_first=True):
        super().__init__(health, attack, defense, name)
        self.attack_first = attack_first
    
class Monster(Unit):
    def __init__(self, health, attack, defense, name, attack_first=False):
        super().__init__(health, attack, defense, name)
        self.attack_first = attack_first

 