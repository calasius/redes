import requests

IP_SERVICE_URL = 'https://freegeoip.net/json/'

resp = requests.get(IP_SERVICE_URL+'129.250.7.69')
if resp.status_code != 200:
	raise ApiError('GET /tasks/ {}'.format(resp.status_code))
print (resp.json()['country_name'])
