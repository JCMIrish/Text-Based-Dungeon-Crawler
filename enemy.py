import random

class Enemy:
    def __init__(self, name, health, attack, loot=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.loot = loot

    def take_damage(self, damage):
        self.health -= damage
        print(f'{self.name} takes {damage} damage! Remaining health: {self.health}')

    def attack_player(self, player):
        damage = random.randint(self.attack - 3, self.attack + 3)
        player.health -= damage
        print(f'{self.name} attacks {player.name} for {damage} damage! {player.name} health: {player.health}')

    def is_alive(self):
        return self.health > 0
    
enemy_types = {
    'goblin': Enemy('Goblin', health=30, attack=5, loot='cracked gem'),
    'skeleton': Enemy('Skeleton', health=50, attack=7, loot='iron shield'),
    'boss': Enemy('Rot King', health=100, attack=12, loot='rotten crown')
}