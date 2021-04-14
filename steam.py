import os
import requests
import argparse

STEAM_KEY = os.environ['STEAM_KEY']

def get_name(*steamids):
    r = requests.get(
            'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/',
            params=dict(
                key=STEAM_KEY,
                steamids=','.join(map(str, steamids))
                )
            )
    return [player['personaname'] for player in r.json()['response']['players']]

def get_owned_games(steamid):
    r = requests.get(
            'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/',
            params=dict(
                key=STEAM_KEY,
                steamid=steamid,
                include_appinfo=True,
                format='json')
            )

    return {game['appid']: game['name'] for game in r.json()['response']['games']}


def get_common(steamid, *steamids):
    ret = get_owned_games(steamid)

    for i2n in map(get_owned_games, steamids):
        ret = {id:name for id, name in ret.items() if id in i2n}

    return ret

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('steamids', type=int, nargs='+', help='steam ids')
    
    args = parser.parse_args()
    print(', '.join(get_name(*args.steamids)))
    for appid, name in get_common(*args.steamids).items():
        print(appid, name)

