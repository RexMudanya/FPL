import requests


def get_data(endpoint):
	""" Get data from api endpoint

	:param endpoint: api url
	:type endpoint: str
	:return: data
	:rtype: dict
	"""
	response = requests.request("GET", url=endpoint)

	return response.json()


# TODO: implement FLP API Authentication to return tokens
