import requests
from key_manager import keys

key = keys['riot_games_api_key']

host                = 'http://52.33.251.214/notification'
url_base            = 'https://global.api.pvp.net{0}'
na_url_base         = 'https://na.api.pvp.net{0}'
provider_url_base   = url_base.format('/tournament/public/v1/provider')
tournament_url_base = url_base.format('/tournament/public/v1/tournament')
code_url_base       = url_base.format('/tournament/public/v1/code')
t_match_url_base    = na_url_base.format('/api/lol/na/v2.2/match/by-tournament/{0}/ids?')
match_info_url_base = na_url_base.format('/api/lol/na/v2.2/match/for-tournament/{0}')
summoner_by_name_base = url_base.format('/api/lol/NA/v1.4/summoner/by-name/{0}')
summoner_league_base = url_base.format("/api/lol/NA/v2.5/league/by-summoner/{0}")
lobby_events_base   = url_base.format('/tournament/public/v1/lobby/events/by-code/{0}')

header = {'X-Riot-Token': key, 'Content-Type': 'application/json'}
header_no_token = {'Content-Type': 'application/json'}

def register_new_provider():
    json_data = {'region': 'NA', 'url': host}
    r = requests.post(provider_url_base, headers=header, json=json_data)
    r.raise_for_status()
    return r.text

provider_id = register_new_provider()

def create_tournament(name):
    json_data = {'name': name, 'providerId': provider_id}
    r = requests.post(tournament_url_base, headers=header, json=json_data)
    r.raise_for_status()
    return r.text

def create_match(tournament_id, num_matches=1, allowed_ids=None, metadata=''):
    params = {'tournamentId': tournament_id, 'count': num_matches}
    json_data = {
        'teamSize': 5,
        'spectatorType': 'ALL',
        'pickType': 'TOURNAMENT_DRAFT',
        'mapType': 'SUMMONERS_RIFT',
        'metadata': metadata
        }
    if allowed_ids is not None:
        json_data['teamSize'] = len(allowed_ids)/2
        json_data['allowedSummonerIds'] = {'participants': allowed_ids}
    r = requests.post(code_url_base, headers=header, params=params,
            json=json_data)
    r.raise_for_status()
    return r.json()[0]

'''Returns summoner name to id. If name does not exist, returns -1'''
def summoner_name_to_id(name):
    # Standardized Summoner Name is all lowercase with spaces removed
    standardized_name = name.lower().replace(" ", "")
    r = requests.get(summoner_by_name_base.format(standardized_name), headers=header)
    r.raise_for_status()
    return r.json()[standardized_name]['id']

'''Gets the lobby events for a specific tounament code'''
def get_lobby_events(tournament_code):
    r = requests.get(lobby_events_base.format(tournament_code), headers=header)
    r.raise_for_status()
    return r.json()

def get_teams(tournament_code):
    import json
    events = get_lobby_events(tournament_code)['eventList']
    events.sort(key=lambda k:k['timestamp'])
    print(json.dumps(events, indent=4))
    leftTeam = [];
    rightTeam = [];
    for event in events:
        print((leftTeam, rightTeam))
        if event['eventType'] == 'PracticeGameCreatedEvent':
            leftTeam.append(event['summonerId'])
        if event['eventType'] == 'PlayerJoinedGameEvent':
            if len(leftTeam) <= len(rightTeam):
                leftTeam.append(event['summonerId'])
            else:
                rightTeam.append(event['summonerId'])
        elif event['eventType'] == 'PlayerSwitchedTeamEvent':
            # Left to right
            try:
                player = leftTeam.pop(leftTeam.index(event['summonerId']))
                rightTeam.append(player)
                continue
            except ValueError:
                # Player is not in leftTeam
                pass
            # Right to left
            try:
                player = rightTeam.pop(rightTeam.index(event['summonerId']))
                leftTeam.append(player)
                continue
            except ValueError:
                # Player is not in rightTeam
                pass
        elif event['eventType'] == 'ChampSelectStartedEvent':
            break
        elif event['eventType'] == 'PlayerQuitGameEvent':
            try:
                leftTeam.remove(event['summonerId'])
            except ValueError:
                pass
            try:
                rightTeam.remove(event['summonerId'])
            except ValueError:
                pass
    return leftTeam, rightTeam

def get_match_id(tournament_code):
    url = t_match_url_base.format(tournament_code)
    r = requests.get(url, headers=header_no_token, params={'api_key': key})
    r.raise_for_status()
    return r.json()[0]

def get_match_info(tournament_code):
    match_id = get_match_id(tournament_code)

    params = {'api_key': key, 'tournamentCode': tournament_code}
    url = match_info_url_base.format(match_id)
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

'''Returns summoner name to info. If name does not exist, returns -1'''
def get_summoner_info(name):
    # Standardized Summoner Name is all lowercase with spaces removed
    standardized_name = name.lower().replace(" ", "")
    r = requests.get(summoner_by_name_base.format(standardized_name), headers=header)
    r.raise_for_status()
    return r.json()[standardized_name]

def get_summoner_league(summoner_id):
    r = requests.get(summoner_league.format(summoner_id), headers=header)
    r.raise_for_status()
    return r.json()[str(summoner_id)];
    

def main():
    # Sample going from beginning to end
    #new_p_id = register_new_provider('Tweeks')
    #t_id = create_tournament('test-tourney', new_p_id)

    # just for now
    # t_id = 1795
    # m_id = 'NA0416f-9b623988-bf60-4a3c-a832-1ce1d0427a65'
    # m_id = create_match(t_id, 1, allowed_names=['Tweeks', 'Teh Crust'])
    # print(m_id)

    # summoner_name_to_id('ShadowLight2143')

    # get_teams(m_id)
    pass

if __name__ == '__main__':
    main()
