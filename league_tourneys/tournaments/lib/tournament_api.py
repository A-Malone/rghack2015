import requests
from key_manager import keys

key = keys['riot_games_api_key']

host = 'http://52.33.251.214'
t_url_base = 'https://global.api.pvp.net{0}'
provider_url_base = t_url_base.format('/tournament/public/v1/provider')
tournament_url_base = t_url_base.format('/tournament/public/v1/tournament')
code_url_base = t_url_base.format('/tournament/public/v1/code')

def register_new_provider(provider_account):
    json_data = {'region': 'NA', 'url': host}
    r = requests.post(provider_url_base, headers=header, json=json_data)

    return r.text

def create_tournament(name, provider_id):
    json_data = {'name': name, 'providerId': provider_id}
    r = requests.post(tournament_url_base, headers=header, json=json_data)

    return r.text

def create_match(tournament_id, num_matches):
    params = {'tournamentId': tournament_id, 'count': num_matches}
    json_data = {
            'teamSize': 5,
            'participants': [0],
            'spectatorType': 'LOBBYONLY',
            'pickType': 'TOURNAMENT_DRAFT',
            'mapType': 'SUMMONERS_RIFT',
            'metadata': ''
            }
    r = requests.post(code_url_base, headers=header, params=params,
            json=json_data)
    return r.text

# Sample going from beginning to end
#new_p_id = register_new_provider('Tweeks')
#t_id = create_tournament('test-tourney', new_p_id)
#m_idcreate_match(t_id, 1)
