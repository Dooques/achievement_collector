import requests
import pandas as pd
import pprint
import json
import os
from xml.etree import ElementTree


class SteamAPI:
    def __init__(self):
        self.api_key = os.environ.get('STEAM_API_KEY')
        self.steam_achievements_endpoint = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/'
        self.steam_games_endpoint = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'\
                                    f'?key={self.api_key}&steamid='
        self.steam_user_data = (f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
                                f'?key={self.api_key}&steamids=')
        userid = 'pallastica'
        steamid_endpoint = f'http://steamcommunity.com/id/{userid}/?xml=1'
        with requests.get(steamid_endpoint) as xml_file:
            root = ElementTree.fromstring(xml_file.text)
            self.steamid = root[0].text

    def get_achievements(self):
        game_lists = self.get_games()
        print(game_lists[1])
        game_dict = {}
        game_dict_final = {}
        index = 0
        for game in game_lists[0]:
            with (requests.get(
                    f'{self.steam_achievements_endpoint}'
                    f'?appid={game}&key={self.api_key}&steamid={self.steamid}'
            ) as raw_file):
                json_file = raw_file.json()
                print("Printing json file")
                print(json_file)
                if 'achievements' in json_file['playerstats']:
                    achievement_count = {achievement['apiname']: True for achievement in json_file['playerstats'][
                        'achievements'] if achievement['achieved'] == 1}
                    game_chieves = {game_lists[1][index]: achievement_count}
                    print('Printing achievement count')
                    print(game_chieves)
                    game_dict.update(game_chieves)
                else:
                    pass
            index += 1
        game_dict_final['game'] = game_dict
        print(game_dict_final)

    def get_games(self):
        with requests.get(f'{self.steam_games_endpoint}{self.steamid}&format=json&include_appinfo=true') as json_file:
            print(json_file.text)
            game_id_list = [item['appid'] for item in json_file.json()['response']['games']]
            game_name_list = [item['name'] for item in json_file.json()['response']['games']]
            return game_id_list, game_name_list

    def get_user_data(self):
        with requests.get(f'{self.steam_user_data}{self.steamid}') as json_file:
            return json_file.text


# item = SteamAPI().get_games()
# print(item)

SteamAPI().get_achievements()
