rooms = {
    'entrance': {
        'description': 'You stand at the entrance of a dark dungeon. Torches flicker on the walls.', 
        'exits': {'north': 'hallway'},
        'enemy': None,
        'item': None
    },
    'hallway': {
        'description': 'A long hallway stretchs before you', 
        'exits': {'north': 'armory', 'east': 'prison', 'south': 'entrance', 'west': 'shop'},
        'enemy': 'goblin',
        'item': None
    },
    'armory': {
        'description': 'Broken weapons line the walls. A rusty word catches your eye', 
        'exits': {'south': 'hallway', 'east': 'cave'},
        'enemy': None,
        'item': 'rusty sword'
    },
        'cave': {
        'description': 'a dark cave with a foul stench.', 
        'exits': {'west': 'armory'},
        'enemy': None,
        'item': None
    },
    'prison': {
        'description': 'Empty cells as far as the eye can see. The air holds a rotten smell', 
        'exits': {'west': 'hallway', 'north': 'throne_room'},
        'enemy': 'skeleton',
        'item': None
    },
    'throne_room': {
        'description': 'A massive throne sits at the far edge of the room. You sense a strong foe', 
        'exits': {'south': 'prison'},
        'enemy': 'boss',
        'item': None
    },
    "shop": {
    "description": "A mysterious merchant sits in the corner. 'Welcome traveler, care to trade?'",
    "exits": {"east": "hallway"},
    "enemy": None,
    "item": None
    },
}