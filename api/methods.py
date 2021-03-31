"""
	code for retrieving data from fpl
"""
from get_data import get_data


class FantasyPremier:
	r"""
	Class to get FPL data from API

	Parameters
	__________
	url : str
		URL path to fpl api

	Attributes
	__________
	url : str
		URL path to fpl api
	general_information : str
		url for general info
	fixtures : str
		fixtures url
	player_data : str
		player data url
	game_week_data : str
		game week data url
	manager_information : str
		manager info url
	manager_history : str
		managers history url
	classic_league_standings : str
		league standings url
	my_team : str
		users/managers team info url

	Methods
	_______
	get_player_data(int) -> dict
		get player data from player/element id
		"fixtures", "history", "history_past"
	get_general_information -> dict
		gets all information of the league divided into
		"events", "game_settings", "phases", "teams",
		"total_players", "elements", "element_stats", "element_types"
	get_fixtures -> dict
		return every fixture of the season
		"event", "team_a", "team_h", "team_a_difficulty",
		"team_h_difficulty", "stats"
	get_game_week_data(int) -> dict
		players information for that specific week
		"id", "stats", "explain"
	get_manager_information(int) -> dict
		returns a user/managers basic information
	get_manager_history(int) -> dict
		return data from previous game-weeks,
		seasons and already used chips
	get_classic_league_standings(int) -> dict
		returns classic league standings
	my_team(int) -> dict
		returns team info
		"picks", "chips", "transfers"

	References
	__________
	`Medium <https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19>`_.

	"""

	def __init__(self, url=None):
		"""Create an instance of class

		:param url: link to the fantasy premier league api
		:type url: str

		:returns: class instance
		:rtype: FantasyPremier
		"""
		if url is None:
			url = 'https://fantasy.premierleague.com/api/'

		self.url = url
		self.general_information = self.url + 'bootstrap-static/'
		self.fixtures = self.url + 'fixtures/'
		self.player_data = self.url + 'element-summary/'  # {element-id}/
		self.game_week_data = self.url + 'event/'  # {event-id}/live/
		self.manager_information = self.url + 'entry/'  # {manager-id}/
		self.manager_history = self.url + 'entry/'  # {manager-id}/history/
		self.classic_league_standings = self.url + 'leagues-classic/'  # league-id}/standings/
		self.my_team = self.url + 'my-team/'  # {manager-id}/

	def get_player_data(self, player_id):
		"""Get players stats

		:param player_id: element-id/players unique identifier
		:rtype player_id: int
		:return: json of players data
		:rtype: dict
		"""
		# TODO: Enter player name instead of id
		url = self.player_data + str(player_id) + "/"
		return get_data(endpoint=url)

	def get_general_information(self):
		""" Get general league info
		:return: leagues general data
		:rtype: dict
		"""
		return get_data(endpoint=self.general_information)

	def get_fixtures(self):
		"""Gets all league fixtures
		:return: fixtures
		:rtype: dict
		"""
		# TODO: get data for a specific fixture/ gameweek fixture
		return get_data(endpoint=self.fixtures)

	def get_game_week_data(self, game_week):
		"""Returns data for a specific game week

		:param game_week: game week number
		:type game_week: int
		:return: data for game week
		:rtype: dict
		"""
		url = self.game_week_data + str(game_week) + "/live/"
		return get_data(endpoint=url)

	def get_manager_information(self, manager_id):
		""" Get a User/Manager info

		:param manager_id: user/manager id
		:type manager_id: int
		:return: data
		:rtype: dict
		"""
		url = self.manager_information + str(manager_id) + "/"
		return get_data(endpoint=url)

	def get_manager_history(self, manager_id):
		""" Manager history

		:param manager_id: user/manager id
		:type manager_id: int
		:return: data
		:rtype: dict
		"""
		url = self.manager_history + str(manager_id) + "/history/"
		return get_data(endpoint=url)

	def get_classic_league_standings(self, league_id):
		""" Table data for H2H

		:param league_id: league identifier
		:type league_id: int
		:return: league data
		:rtype: dict
		"""
		# TODO: Enter League name instead of id
		url = self.classic_league_standings + str(league_id) + "/standings/"
		return get_data(endpoint=url)

	def get_my_team(self, team_id):
		""" User/Managers Team data
		:param team_id: team identifier
		:type team_id: int
		:return: team info
		:rtype: dict
		"""
		# TODO: Create authentication for this function
		url = self.my_team + str(team_id) + "/"
		return get_data(endpoint=url)
