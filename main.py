'''
Project Title: TBDC - A simple Text Based Adventure
Description: A text based adventure where you stumble into a dungeon slay a few foes and confront the King of Rot. Do you have the Strength to face such a foe?

Developed by: JCMIrish                                                                                   
GitHub: https://github.com/JCMIrish        
License: MIT                                                                                                    
'''
import random
from time import sleep

from rooms import rooms
from items import items
from player import Player
from enemy import Enemy, enemy_types

def describe_room(room_name):
    room = rooms[room_name]
    print('\n' + '='*40)
    print(room['description'])
    print(f'Exits: {'. '.join(room['exits'].keys())}')
    if room['item']:
        print(f'You notice something here: {room['item']}')
    if room['enemy']:
        enemy = enemy_types[room['enemy']]
        if enemy.is_alive():
            print(f'warning a {room['enemy']} blocks your path!')
        else:
            print(f'The corpse of a {room['enemy']} lies here.')
    print('='*40)

def move(current_room, direction):
    room = rooms[current_room]
    if direction in room['exits']:
        return room['exits'][direction]
    else:
        print("you can't go in that direction")
        return current_room
    
def combat(player, enemy):
    print(f'\nCombat starts between {player.name} and {enemy.name}!')
    
    while player.is_alive() and enemy.is_alive():
        print('\n[1] Attack [2] Run')
        choice = input('Choose your action: ')
        
        if choice == '1':
            damage = random.randint(player.attack - 3, player.attack + 3)
            enemy.take_damage(damage)

            if enemy.is_alive():
                enemy.attack_player(player)
            else:
                print(f'You defeated the {enemy.name}!')
                if enemy.loot:
                    print(f'You found {enemy.loot} on the {enemy.name}!')
                    player.pick_up(enemy.loot)
                gold_earned = random.randint(5, 15)
                player.gold += gold_earned
                print(f'You earned {gold_earned} gold! Total gold: {player.gold}')

        elif choice == '2':
            print('You attempt to flee...')
            if random.random() < 0.5:
                print('You successfully escaped!')
                return 'fled'
            else:
                print('Failed to escape! The enemy attacks you as you flee.')
                enemy.attack_player(player)
        else:
            print('Invalid choice. Please choose 1 or 2.')

        if not player.is_alive():
            print('You have been defeated! Game Over.')
            return 'dead'
        
    return 'victory'

def shop(player):
    print('\n welcome to the shop!')
    print('------------------------')
    print('your gold: ', player.gold)
    print('[1] Health Potion (10 gold) - Restores 20 health')
    print('[2] Sharp Sword (15 gold) - Increases attack by 5 permanently')
    print('[3] Sell items')
    print('[4] Leave shop')
    print('------------------------')

    while True:
        choice = input('What would you like to buy? ').strip()
        if choice == '1':
            if player.gold >= 10:
                player.gold -= 10
                player.health += 20
                print('You bought a Health Potion! Your health is now:', player.health)
            else:
                print('Not enough gold!')
        elif choice == '2':
            if player.gold >= 15:
                if "sharp sword" in player.inventory:
                    print('You already have a Sharp Sword!')
                else:
                    player.gold -= 15
                    player.pick_up('sharp sword')
                    player.equip('sharp sword')
                    print('You bought a Sharp Sword! Your attack is now:', player.attack)
            else:
                print('Not enough gold!')
        elif choice == '3':
            found = False
            if "cracked gem" in player.inventory:
                value = items["cracked gem"]["gold_value"]
                player.inventory.remove("cracked gem")
                player.gold += value
                print(f'You sold a cracked gem for {value} gold! Your gold is now:', player.gold)
                found = True
            if "rusty sword" in player.inventory:
                confirm = input('Do you want to sell your rusty sword? (y/n) ').strip().lower()
                if confirm == 'y':
                    value = items["rusty sword"]["gold_value"]
                    if player.equipped == "rusty sword":
                        player.unequip("rusty sword")
                    player.inventory.remove("rusty sword")
                    player.gold += value
                    print(f'You sold a rusty sword for {value} gold! Your gold is now:', player.gold)
                    found = True
                else:
                    print('You decided to keep the rusty sword.')
                    found = True
            if not found:
                print('You have nothing to sell!')
        elif choice == '4':
            print('Leaving shop...')
            break
        else:
            print('Invalid choice.')

def save_score(player, outcome):
    with open('scores.txt', 'a') as f:
        f.write(f'{player.name} | {outcome} | Health: {player.health} | Gold: {player.gold} | Inventory: {", ".join(player.inventory) if player.inventory else "Empty"}\n')
    print('Score saved to scores.txt!')

def title_screen():
    print('='*40)
    print('Welcome to the Dungeon!')
    print('='*40)
    print('[1] Start Game')
    print('[2] View Scores')
    print('[3] Quit')
    print('='*40)
    choice = input('Choose an option: ')
    if choice == '1':    
        return True
    elif choice == '2':
        try:
            with open('scores.txt', 'r') as f:
                print('\n--- Previous Scores ---')
                print(f.read())
        except FileNotFoundError:
            print('No scores found.')
        return title_screen()
    elif choice == '3':
        print('Goodbye!')
        exit()
    else:
        print('Invalid choice. Please try again.')
        return title_screen()

title_screen()

def game_loop():
    print('welcome to the dungeon')
    player_name = input('Enter your adventurers name: ')
    player = Player(player_name)
    print(f'\nGood luck, {player_name}. and watch youself\n')

    current_room = 'entrance'
    previous_room = 'entrance'

    while True:
        describe_room(current_room)
        action = input('\nWhat do you do? (move [direction] | stats | pickup | equip | quit): ').strip().lower()

        if action == 'quit':
            print('you flee in cowardice')
            save_score(player, "Quit")
            break
        elif action == 'stats':
            player.show_stats()
        elif action == 'pickup':
            room = rooms[current_room]
            if room['item']:
                player.pick_up(room['item'])
                room['item'] = None
            else:
                print('No items to pick up here')
        elif action.startswith('equip'):
            parts = action.split(" ", 1)
            if len(parts) < 2:
                equipable = [i for i in player.inventory if items.get(i) and items[i]['slot']]
                if equipable:
                    print(f"Equip what? You have: {', '.join(equipable)}")
                else:
                    print("You have nothing equipable.")
            else:
                item_name = parts[1]
                player.equip(item_name)
        elif action.startswith('move'):
            parts = action.split(" ")
            if len(parts) < 2:
                print("Move where? Try: move north")
            else:
                direction = parts[1]
                new_room = move(current_room, direction)

                if new_room != current_room:
                    previous_room = current_room # Update previous room before moving
                    current_room = new_room

                    if current_room == 'shop':
                        shop(player)

                    room = rooms[current_room]
                    
                    if room['enemy']:
                        enemy_name = room['enemy']
                        enemy = enemy_types[enemy_name]

                        if enemy.is_alive():
                            result = combat(player, enemy)
                            
                            if result == 'dead':
                                print('\nGame Over!')
                                print(f'you made it to the {current_room} before dying.')
                                save_score(player, "defeated")
                                sleep(5)
                                break
                            elif result == 'victory' and current_room == 'throne_room':
                                print('\nYou win!')
                                print(f'you defeated the Rot King {player.name}!')
                                print(f'Final stats - Health: {player.health} | Gold: {player.gold} | Inventory: {", ".join(player.inventory) if player.inventory else "Empty"}')
                                save_score(player, "victory")
                                sleep(5)
                                break
                            elif result == 'fled':  
                                current_room = previous_room # Move back to previous room")
        else:
            print('Unknown command. Try again or quit')

game_loop()
