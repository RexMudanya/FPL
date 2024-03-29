from methods import FantasyPremier


class Player:
	"""
	class for player methods to access various data

	Parameters
	__________
	url : str
		URL path to fpl api

	Attributes
	__________
	fpl : FantasyPremier
		object of FPL API

	Methods
	_______
	get_all_data -> dict
		gets all player data
		"fixtures", "history", "history_past"

	get_gm_wk_data(int, int) -> dict
		gets all data for a specified game week
		'element', 'fixture', 'opponent_team', 'total_points', 'was_home', 'kickoff_time',
		'team_h_score', 'team_a_score', 'round', 'minutes', 'goals_scored',
		'assists', 'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed',
		'yellow_cards',
		'red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat', 'ict_index', 'value',
		'transfers_balance', 'selected', 'transfers_in', 'transfers_out'

	get_fixtures(int) -> list
		gets players fixtures
		returns a list of dicts containing keys:
		id
		code
		team_h
		team_h_score
		team_a
		team_a_score
		event
		finished
		minutes
		provisional_start_time
		kickoff_time
		event_name
		is_home
		difficulty

	get_past_history(int) -> list
		returns a players past seasons history as a dict in a list
		with the following keys:
		season_name
		element_code
		start_cost
		end_cost
		total_points
		minutes
		goals_scored
		assists
		clean_sheets
		goals_conceded
		own_goals
		penalties_saved
		penalties_missed
		yellow_cards
		red_cards
		saves
		bonus
		bps
		influence
		creativity
		threat
		ict_index

	"""

	def __init__(self, url=None):
		"""
		creates class instance
		:param url: path to api
		:type url: str
		:rtype: Player
		"""
		self.fpl = FantasyPremier(url)

	def get_all_data(self, player_id):
		""" return all data
		:param player_id: element id
		:type player_id: int
		:return: data
		:rtype: dict
		"""
		return self.fpl.get_player_data(player_id)

	def get_gm_wk_data(self, player_id, game_week):
		"""
		returns game week data
		:param player_id: element id
		:type player_id: int
		:param game_week: specified gm week
		:type game_week: int
		:return: game week data
		:rtype: dict
		"""
		return self.get_all_data(player_id)["history"][int(game_week - 1)]

	def get_fixtures(self, player_id):
		"""
		returns players fixtures
		:param player_id: element id
		:type player_id: int
		:return: fixtures in a list of dicts
		:rtype: list
		"""
		return self.get_all_data(player_id)["fixtures"]

	def get_past_history(self, player_id):
		"""
		returns players past history
		:param player_id: element id
		:return: past seasons history
		:rtype: list
		"""
		return self.get_all_data(player_id)["history_past"]


class Viz:
	"""
	methods to plot various player data
	"""

	def __init__(self, url=None):
		self.player = Player(url)

	def plot_value(self):
		pass

	def plot_points(self):
		pass

	def plot_transfer_history(self):
		pass
