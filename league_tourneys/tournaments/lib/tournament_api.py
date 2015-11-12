import requests
from key_manager import keys

key = keys['riot_games_api_key']

host                = 'http://52.33.251.214'
url_base            = 'https://global.api.pvp.net{0}'
provider_url_base   = url_base.format('/tournament/public/v1/provider')
tournament_url_base = url_base.format('/tournament/public/v1/tournament')
code_url_base       = url_base.format('/tournament/public/v1/code')
t_match_url_base    = url_base.format('/api/lol/NA/v2.2/match/for-tournament/{0}')

header = {'X-Riot-Token': key, 'Content-Type': 'application/json'}

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
            'spectatorType': 'ALL',
            'pickType': 'TOURNAMENT_DRAFT',
            'mapType': 'SUMMONERS_RIFT',
            'metadata': ''
            }
    r = requests.post(code_url_base, headers=header, params=params,
            json=json_data)
    return r.json()[0]

def get_initial_info(match_id):
    url = match_url_base.format(match_id)
    #r = requests.get(url, 



# Sample going from beginning to end
#new_p_id = register_new_provider('Tweeks')
#t_id = create_tournament('test-tourney', new_p_id)

# just for now
t_id = 1795
m_id = 'NA0416f-ab701d93-089d-4c34-bf5a-0cd2193b0cef'
#m_id = create_match(t_id, 1)
print m_id
