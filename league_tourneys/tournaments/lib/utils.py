import datetime as dt
import tournament_api as r_api

def register_new_provider(provider_account):
    return r_api.register_new_provider(provider_account)

def create_tournament(name, provider_id):
    return r_api.create_tournament(name, provider_id)

def create_match(tournament_code):
    return r_api.create_match(tournament_code)

def get_match_id(tournament_code):
    return r_api.get_match_id(tournament_code)

def get_match_info(tournament_code):
    return r_api.get_match_info(tournament_code)

def get_winner_id(info):
    teams = info['teams']
    winner_id = teams[0]['teamId'] if teams[0]['winner'] else teams[1]['teamId']
    return winner_id

def get_team_info(tournament_code, team_id=100):
    team_info = {}
    team_info['winner'] = False

    info = get_match_info(tournament_code)
    if team_id == get_winner_id(info):
        team_info['winner'] = True

    team = info['teams'][0] if info['teams'][0]['teamId'] == team_id else info['teams'][1]

    team_info['tower_kills'] = team['towerKills']
    team_info['baron_kills'] = team['baronKills']
    team_info['dragon_kills'] = team['dragonKills']
    team_info['gold'] = 0

    participants = info['participants']
    participants_id = info['participantIdentities']

    team_list = [x for x in participants if x['teamId'] == team_id]

    player_info_list = []

    for player in team_list:
        stats = player['stats']
        p_id = player['participantId']
        p_id_info = [x for x in participants_id if x['participantId'] ==
                p_id][0]['player']

        player_info = {
                'summoner'  : p_id_info['summonerName'],
                'icon'      : p_id_info['profileIcon'],
                'champ_id'  : player['championId'],
                'champ_name': '',
                'champ_lvl' : stats['champLevel'],
                'spell_ids' : (player['spell1Id'], player['spell2Id']),
                'kills'     : stats['kills'],
                'deaths'    : stats['deaths'],
                'assists'   : stats['assists'],
                'item_ids'  : [v for k,v in stats.iteritems() if
                    k.startswith('item')],
                'cs'        : stats['minionsKilled'] +
                    stats['neutralMinionsKilledTeamJungle'] +
                    stats['neutralMinionsKilledEnemyJungle'],
                'gold'      : stats['goldEarned']

        }
        team_info['gold'] += stats['goldEarned']
        player_info_list.append(player_info)

    team_info['player_info'] = player_info_list
    return team_info

def get_game_times(tournament_code):
    info = get_match_info(tournament_code)
    game_info = {}

    # division because the API call gives timestamp in milliseconds
    dt_obj = dt.datetime.fromtimestamp(info['matchCreation']/1000)
    dt_str = '{0}/{1}/{2} - {3}:{4}'.format(dt_obj.day, dt_obj.month,
            dt_obj.year, dt_obj.hour, dt_obj.minute)

    game_info['date'] = dt_str
    game_info['duration'] = str(dt.timedelta(seconds=info['matchDuration']))
    if game_info['duration'][0] == '0':
        game_info['duration'] = game_info['duration'].split(':', 1)[1]

    return game_info
