from items import items

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 10
        self.gold = 0
        self.inventory = []
        self.equipped = {
            'weapon': None,
            'armor': None
        }


    def show_stats(self):
        print('\n--- Player Stats ---')
        print(f'Name: {self.name}')
        print(f'Health: {self.health}')
        print(f'Attack: {self.attack}')
        print(f'Gold: {self.gold}')
        print(f"weapon: {self.equipped['weapon'] if self.equipped['weapon'] else 'Nothing'}")
        print(f"armor: {self.equipped['armor'] if self.equipped['armor'] else 'Nothing'}")
        print(f'Inventory: {", ".join(self.inventory) if self.inventory else "Empty"}')
        print('-------------------')

    def pick_up(self, item_name):
        if item_name in self.inventory:
            print(f"You already have a {item_name}!")
            return
        self.inventory.append(item_name)
        print(f"You picked up: {item_name}")

    def equip(self, item_name):
        if item_name not in self.inventory:
            print(f"You don't have a {item_name}!")
            return

        item = items.get(item_name)
        if not item or not item["slot"]:
            print(f"The {item_name} cannot be equipped.")
            return

        slot = item["slot"]

        # Unequip current item in that slot first
        if self.equipped[slot]:
            self._apply_item(self.equipped[slot], remove=True)
            print(f"You unequipped the {self.equipped[slot]}.")

        # Equip new item
        self._apply_item(item_name)
        self.equipped[slot] = item_name
        print(f"You equipped the {item_name}!")
        print(f"Attack: {self.attack} | Health: {self.health}")


    def unequip(self, item_name):
        item = items.get(item_name)
        if not item or not item["slot"]:
            return
        slot = item["slot"]
        if self.equipped[slot] == item_name:
            self._apply_item(item_name, remove=True)
            self.equipped[slot] = None
            print(f"You unequipped the {item_name}.")

    def _apply_item(self, item_name, remove=False):
        if item_name in items:
            item = items[item_name]
            modifier = -1 if remove else 1
            self.attack += item["attack_bonus"] * modifier
            self.health += item["health_bonus"] * modifier

    def is_alive(self):
        return self.health > 0