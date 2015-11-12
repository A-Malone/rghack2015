import requests
from key_manager import keys

api_key = keys['challonge_api_key']

'''http://api.challonge.com/v1/documents/tournaments/create'''
def create_tournament(tournament={}):
	data = {'api_key':api_key, 'tournament':tournament}
	r = requests.post('https://challonge.com/api/tournaments.json', json=data)
	return r.json()

'''http://api.challonge.com/v1/documents/tournaments/show'''
def show_tournament(tournament_id, include_participants=False, include_matches=False):
	data = {'api_key':api_key}
	r = requests.get('https://api.challonge.com/v1/tournaments/{}.json'.format(tournament_id), params=data)
	return r.json()

'''http://api.challonge.com/v1/documents/participants/create'''
def create_participant(tournament_id, participant={}):
	data = {'api_key':api_key, 'participant':participant}
	r = requests.post('https://api.challonge.com/v1/tournaments/{}/participants.json'.format(tournament_id), json=data)
	return r.json()

'''http://api.challonge.com/v1/documents/participants/randomize'''
def randomize_seeds(tournament_id):
	data = {'api_key':api_key}
	r = requests.post('https://api.challonge.com/v1/tournaments/{}/participants/randomize.json'.format(tournament_id), json=data)
	return r.json()

'''http://api.challonge.com/v1/documents/tournaments/start'''
def start_tournament(tournament_id, include_participants=False, include_matches=False):
	data = {'api_key':api_key, 'include_participants':int(include_participants), 'include_matches':int(include_matches)}
	r = requests.post('https://api.challonge.com/v1/tournaments/{}/start.json'.format(tournament_id), json=data)
	return r.json()

def finalize_tournament(tournament_id):
	data = {'api_key':api_key}
	r = requests.post('https://api.challonge.com/v1/tournaments/{}/finalize.json'.format(tournament_id), json=data)
	return r.json()

'''http://api.challonge.com/v1/documents/matches/index'''
def get_match_list(tournament_id, state="all", participant_id=None):
	data = {'api_key':api_key, 'state':state}
	if participant_id is not None:
		data['participant_id'] = participant_id
	r = requests.get('https://api.challonge.com/v1/tournaments/{}/matches.json'.format(tournament_id), params=data)
	return r.json()

'''http://api.challonge.com/v1/documents/match_attachments/create'''
def create_match_attachment(tournament_id, match_id, match_attachment={}):
	data = {'api_key':api_key, 'match_attachment':match_attachment}
	r = requests.post('https://api.challonge.com/v1/tournaments/{}/matches/{}/attachments.json'.format(tournament_id, match_id), json=data)
	return r.json()

'''http://api.challonge.com/v1/documents/matches/update'''
def update_match(tournament_id, match_id, match={}):
	data = {'match':match}
	r = requests.put('https://api.challonge.com/v1/tournaments/{}/matches/{}.json'.format(tournament_id, match_id), json=data)

def main():		
	# Create tournament
	tournament = {'name':'API Tournament 1',
		#'tournament_type':'single elimination',
	    'url':'API_t_1',
		'description':'a description',
		'open_signup':'false',
		'ranked_by':'match wins',
		'hide_forum':'true',
		'private':'true',
		'signup_cap':'10'};
	c = create_tournament(tournament)
	print(c)
	t_id = c['tournament']['id'];

	# Create participants (loop this k)
	participant = {'name':'participant A'}
	p = create_participant(t_id, participant)
	print(p)
	participant = {'name':'participant B'}
	p = create_participant(t_id, participant)
	print(p)

	# Randomize seeds
	r = randomize_seeds(t_id)
	print(r)

	# Start tournament
	s = start_tournament(t_id)
	print(s)

	# Check matches
	ml = get_match_list(t_id)
	print(ml)

	# Win the match
	match = {"scores_csv":"1-0","winner_id":p['participant']['id']};
	u = update_match(t_id, ml[0], match)

	# End the tournament
	finalize_tournament(t_id)


if __name__ == '__main__':
	main()