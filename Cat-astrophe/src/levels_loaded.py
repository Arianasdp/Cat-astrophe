import json
# from game_data import levels

# with open('partida_guardada.json', 'w') as file:
#     json.dump(levels, file)

# with open('partida_guardada.json', 'r') as file:
#     levels_loaded = json.load(file)

saved_game = 'partida_guardada.json'

def save_current_level(current_level):
    with open(saved_game, 'w') as file:
        json.dump(current_level, file)

def load_saved_level():
    try:
        with open(saved_game, 'r') as file:
            saved_file = json.load(file)
        return saved_file
    except FileNotFoundError:
        return None
