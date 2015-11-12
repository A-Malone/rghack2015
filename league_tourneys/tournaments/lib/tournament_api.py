import requests
from key_manager import keys

key = keys['riot_games_api_key']

host                = 'http://52.33.251.214'
url_base            = 'https://global.api.pvp.net{0}'
na_url_base         = 'https://na.api.pvp.net{0}'
provider_url_base   = url_base.format('/tournament/public/v1/provider')
tournament_url_base = url_base.format('/tournament/public/v1/tournament')
code_url_base       = url_base.format('/tournament/public/v1/code')
t_match_url_base    = na_url_base.format('/api/lol/na/v2.2/match/by-tournament/{0}/ids?')
match_info_url_base = na_url_base.format('/api/lol/na/v2.2/match/for-tournament/{0}')
summoner_by_name_base = url_base.format('/api/lol/NA/v1.4/summoner/by-name/{0}')
lobby_events_base   = url_base.format('/tournament/public/v1/lobby/events/by-code/{0}')

header = {'X-Riot-Token': key, 'Content-Type': 'application/json'}
header_no_token = {'Content-Type': 'application/json'}

def register_new_provider(provider_account):
    json_data = {'region': 'NA', 'url': host}
    r = requests.post(provider_url_base, headers=header, json=json_data)

    return r.text

def create_tournament(name, provider_id):
    json_data = {'name': name, 'providerId': provider_id}
    r = requests.post(tournament_url_base, headers=header, json=json_data)

    return r.text

def create_match(tournament_id, num_matches=1, participants=[0], metadata=''):
    params = {'tournamentId': tournament_id, 'count': num_matches}
    json_data = {
            'teamSize': 5,
            'participants': participants,
            'spectatorType': 'ALL',
            'pickType': 'TOURNAMENT_DRAFT',
            'mapType': 'SUMMONERS_RIFT',
            'metadata': metadata
            }
    r = requests.post(code_url_base, headers=header, params=params,
            json=json_data)
    return r.json()[0]

'''Returns summoner name to id. If name does not exist, returns -1'''
def summoner_name_to_id(name):
    # Standardized Summoner Name is all lowercase with spaces removed
    standardized_name = name.lower().replace(" ", "")
    r = requests.get(summoner_by_name_base.format(standardized_name), headers=header)
    # Summoner not found
    if r.status_code == '404':
        return -1
    return r.json()[standardized_name]['id']

'''Gets the lobby events for a specific tounament code'''
def get_lobby_events(tournament_code):
    r = requests.get(lobby_events_base.format(tournament_code), headers=header)
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
    match_id = r.json()[0]
    return match_id

def get_match_info(tournament_code):
    match_id = get_match_id(tournament_code)

    params = {'api_key': key, 'tournamentCode': tournament_code}
    url = match_info_url_base.format(match_id)
    r = requests.get(url, params=params)
    match_info = r.json()
    return match_info

def main():
    # Sample going from beginning to end
    #new_p_id = register_new_provider('Tweeks')
    #t_id = create_tournament('test-tourney', new_p_id)

    # just for now
    t_id = 1795
    m_id = 'NA0416f-9b623988-bf60-4a3c-a832-1ce1d0427a65'
    #m_id = create_match(t_id, 1)
    print(m_id)

    summoner_name_to_id('ShadowLight2143')

    get_teams(m_id)

if __name__ == '__main__':
    main()