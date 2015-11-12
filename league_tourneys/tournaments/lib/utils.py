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
        player_info_list.append(player_info)

    team_info['player_info'] = player_info_list
    return team_info
