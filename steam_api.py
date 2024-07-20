import requests
import pprint
import json
import os
from xml.etree import ElementTree


def sort_achievements(data):
    achievement_dict = {}
    try:
        if data['game']['availableGameStats']['achievements']:
            for achievement in data['game']['availableGameStats']['achievements']:
                achievement_dict[achievement['name']] = {
                    'displayName': achievement['displayName'],
                    'description': achievement['description'],
                    'img_url': achievement['icon']
                }
            return achievement_dict
        elif data['game']['achievements']:
            for achievement in data['game']['achievements']:
                achievement_dict[achievement['name']] = {
                    'displayName': achievement['displayName'],
                    'description': achievement['description'],
                    'img_url': achievement['icon']
                }
            return achievement_dict
    except KeyError:
        pass


class SteamAPI:
    def __init__(self):
        self.api_key = os.environ.get('STEAM_API_KEY')
        self.player_achievements_endpoint = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/'
        self.steam_games_endpoint = (f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
                                     f'?key={self.api_key}&steamid=')
        self.steam_user_data = (f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
                                f'?key={self.api_key}&steamids=')
        self.game_data = (f'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v0002?key={self.api_key}'
                          f'')
        userid = 'Samstarscream'
        steamid_endpoint = f'http://steamcommunity.com/id/{userid}/?xml=1'
        with requests.get(steamid_endpoint) as xml_file:
            root = ElementTree.fromstring(xml_file.text)
            self.steamid = root[0].text

    def get_achievements(self):
        user_game_data = self.get_user_game_data()
        index = 0
        for game in user_game_data.values():
            print(game)
            with requests.get(
                    f'{self.player_achievements_endpoint}'
                    f'?appid={game['appid']}'
                    f'&key={self.api_key}'
                    f'&steamid={self.steamid}') as raw_file:
                json_file = raw_file.json()
                try:
                    if 'achievements' in json_file['playerstats']:
                        for achievement in json_file['playerstats']['achievements']:
                            if achievement['achieved'] == 1:
                                print(f'Achievement Unlocked: {game['achievements'][achievement['apiname']]}')
                                game['achievements'][achievement['apiname']]['achieved'] = True
                            elif achievement['achieved'] == 0:
                                print(f'Achievement Locked: {game['achievements'][achievement['apiname']]}')
                                game['achievements'][achievement['apiname']]['achieved'] = False
                            else:
                                pass
                    else:
                        pass
                except TypeError:
                    pass
            index += 1
        with open('game_data.json', 'w') as json_file:
            json.dump(user_game_data, json_file, indent=4)
            return user_game_data

    def get_games(self):
        with (requests.get(f'{self.steam_games_endpoint}{self.steamid}&format=json&include_appinfo=true') as raw_file):
            json_file = raw_file.json()
            print(json_file['response'])
            game_id_list = [item['appid'] for item in json_file['response']['games']]
            game_name_list = [item['name'] for item in json_file['response']['games']]
            game_url_hash = [f"https://media.steampowered.com/steamcommunity/public/images/apps/{item['appid']}/"
                             f"{item['img_icon_url']}.jpg" for item in json_file['response']['games']]
            return game_id_list, game_name_list, game_url_hash

    def get_user_data(self):
        with requests.get(f'{self.steam_user_data}{self.steamid}&format=json') as json_file:
            return json_file.text

    def get_user_game_data(self):
        game_lists = self.get_games()
        index = 0
        user_games_dict = {}
        for game in game_lists[0]:
            with requests.get(f'{self.game_data}&appid={game}') as raw_file:
                json_data = raw_file.json()
                if 'gameName' in json_data['game'] and json_data['game']['gameName'] == game_lists[1][index]:
                    game_dict = {
                        'gameName': json_data['game']['gameName'],
                        'appid': game_lists[0][index],
                        'img_url_hash': game_lists[2][index]
                    }
                    print(json_data)
                    achievement_list = sort_achievements(json_data)
                    game_dict['achievements'] = achievement_list
                    user_games_dict[json_data['game']['gameName']] = game_dict
                else:
                    pass
                index += 1
        return user_games_dict
