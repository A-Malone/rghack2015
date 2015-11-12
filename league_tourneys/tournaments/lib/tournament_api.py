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

def create_match(tournament_code, num_matches):
    params = {'tournamentId': tournament_code, 'count': num_matches}
    json_data = {
            'teamSize': 5,
            'participants': [0],
            'spectatorType': 'ALL',
            'pickType': 'TOURNAMENT_DRAFT',
            'mapType': 'SUMMONERS_RIFT',
            'metadata': ''
            }
    r = requests.post(code_url_base, headers=header, params=params,
            json=json_data)
    return r.json()[0]

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
