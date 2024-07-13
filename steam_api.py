import requests
import pprint
import json
import os
from xml.etree import ElementTree


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
        print(f'{user_game_data} \n')
        for game in user_game_data.values():
            print(f'game_data: {game}\n')
            with requests.get(
                    f'{self.player_achievements_endpoint}'
                    f'?appid={game['appid']}'
                    f'&key={self.api_key}'
                    f'&steamid={self.steamid}') as raw_file:
                json_file = raw_file.json()
                print(f'Data received: {json_file}\n')
                if 'achievements' in json_file['playerstats']:
                    for achievement in json_file['playerstats']['achievements']:
                        if achievement['achieved'] == 1:
                            game['achievements'][achievement['apiname']]['achieved'] = True
                        else:
                            game['achievements'][achievement['apiname']]['achieved'] = False
                    print(f'updated_data: {game}\n')
                else:
                    pass
            index += 1
        with open('game_data.json', 'w') as json_file:
            json.dump(user_game_data, json_file, indent=4)

    def get_games(self):
        with requests.get(f'{self.steam_games_endpoint}{self.steamid}&format=json&include_appinfo=true') as json_file:
            game_id_list = [item['appid'] for item in json_file.json()['response']['games']]
            game_name_list = [item['name'] for item in json_file.json()['response']['games']]
            game_url_hash = [item['img_icon_url'] for item in json_file.json()['response']['games']]
            return game_id_list, game_name_list, game_url_hash

    def get_user_data(self):
        with requests.get(f'{self.steam_user_data}{self.steamid}&format=json') as json_file:
            return json_file.text

    def get_user_game_data(self):
        game_lists = self.get_games()
        index = 0
        user_games_dict = {}
        for game in game_lists[0][:6]:
            with requests.get(f'{self.game_data}&appid={game}') as raw_file:
                json_data = raw_file.json()
                if 'gameName' in json_data['game'] and json_data['game']['gameName'] == game_lists[1][index]:
                    game_dict = {
                        'gameName': json_data['game']['gameName'],
                        'appid': game_lists[0][index],
                        'img_url_hash': game_lists[2][index]
                    }
                    achievement_list = self.sort_achievements(json_data)
                    # print(f'achievements_list: {achievement_list}')
                    game_dict['achievements'] = achievement_list
                    # print(f'Creating game_dict: {game_dict}')
                    user_games_dict[json_data['game']['gameName']] = game_dict
                else:
                    pass
                index += 1
        #         print(f'user_games_dict updated: {user_games_dict}')
        # print(f'Printing final dict:')
        return user_games_dict

    def sort_achievements(self, data):
        achievement_dict = {}
        # print(f'sorting achievements: {data['game']}')
        try:
            if data['game']['availableGameStats']['achievements']:
                # print(f'Adding {data["game"]["gameName"]} achievements')
                for achievement in data['game']['availableGameStats']['achievements']:
                    # print(f'adding {achievement}')
                    achievement_dict[achievement['name']] = {
                        'displayName': achievement['displayName'],
                        'description': achievement['description'],
                        'img_url': achievement['icon']
                    }
                # print(f'creating achievement dict: {achievement_dict}')
                return achievement_dict
            elif data['game']['achievements']:
                # print(f'Adding {data["game"]["gameName"]}')
                for achievement in data['game']['achievements']:
                    achievement_dict[achievement['name']] = {
                        'displayName': achievement['displayName'],
                        'description': achievement['description'],
                        'img_url': achievement['icon']
                    }
                # print(f'creating achievement dict: {achievement_dict}')
                return achievement_dict
        except KeyError:
            pass

# item = SteamAPI().get_games()
# print(item)


SteamAPI().get_achievements()

