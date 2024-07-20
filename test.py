import json
from pprint import pprint


with open('game_data.json', 'r') as json_file:
    game_data = json.load(json_file)
    game_list = [game for game in game_data.values()]
    new_game_list = []
    achievement_dict = {}
    for game in game_list:
        new_game_list.append(game)
        if game['achievements'] is None:
            pass
        else:
            current_game = {game['gameName']: 'achievements available'}
            achievements = [achievement for achievement in game['achievements'].values()]
            print(achievements)
            for num in range(5):
                achievement_dict[game['gameName']] = achievements[:5]
    pprint(f'achieve values: {achievement_dict}')
