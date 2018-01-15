
import telegram
from time import sleep
import json
import csv
import http.client

BOT_TOKEN = "412388726:AAFtMuVKwPGCjZ_QTF_oDjAhYHbrSeeMcec"
Bot = telegram.Bot(BOT_TOKEN)
last_msg_id = 0

WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000

def widen(s):
	return s.translate(WIDE_MAP)

def get_team_id_json(team_name):
	json_data = open("/Users/manchunglo/Desktop/tg_bot/team_id.json").read()
	data = json.loads(json_data)
	result_string = ""
	counter = 0
	for each in data:
		try:
			return([each[team_name.lower()], data])
		except:
			continue
	return

def get_csv_online():
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': 'ef04198579bd495f9f17a1651500a430', 'X-Response-Control': 'minified' }
	connection.request('GET', '/v1/competitions/445/fixtures', None, headers )
	response = json.loads(connection.getresponse().read())
	for team in response['fixtures']:
		print(team["homeTeamName"] + " " + str(team["result"]["goalsAwayTeam"]) + " : " + \
			str(team["result"]["goalsHomeTeam"]) + " " + team["awayTeamName"])
	return

def get_team_id():
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': 'ef04198579bd495f9f17a1651500a430', 'X-Response-Control': 'minified' }
	connection.request('GET', '/v1/competitions/445/teams', None, headers )
	response = json.loads(connection.getresponse().read())
	result_string = ""
	for team in response['teams']:
		result_string += str(team["id"]) + " " + team["name"]
	return result_string

def id_to_name(id_list, team_id):
	for name in id_list:
		try:
			return name[str(team_id)]
		except:
			continue
	return

def get_team_score(team_name):
	team_info = get_team_id_json(team_name)
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': 'ef04198579bd495f9f17a1651500a430', 'X-Response-Control': 'minified' }
	connection.request('GET', '/v1/teams/' + str(team_info[0]) + '/fixtures', None, headers )
	response = json.loads(connection.getresponse().read())
	counter = 0
	line_new = ""
	for team in reversed(response['fixtures']):
		if team["status"] == 'FINISHED' and counter < 5:
			home_name = id_to_name(team_info[1], team["homeTeamId"])
			away_name = id_to_name(team_info[1], team["awayTeamId"])

			if len(home_name) == 4:
				home_name = home_name.ljust(7)
			elif len(home_name) == 2:
				home_name = home_name.ljust(13)
			else:
				home_name = home_name.ljust(10)

			if len(away_name) == 4:
				away_name = away_name.ljust(7)
			elif len(away_name) == 2:
				away_name = away_name.ljust(13)
			else:
				away_name = away_name.ljust(10)
			result = str(team["result"]["goalsHomeTeam"]) + \
						":" + str(team["result"]["goalsAwayTeam"])
			line_new += team["date"][:10].ljust(15) + home_name + \
						widen(result).ljust(10) + away_name + "\n"
			counter += 1
	return line_new

def get_chat_id(Update):
	return Update["message"]["chat"]["id"]
def get_user_id(Update):
	return Update["message"]["from_user"]["id"]

def get_text(Update):
	return Update["message"]["text"]

def get_msg_id(Update):
	return Update["update_id"]

def msg_handler(Update):
	global last_msg_id
	text = get_text(Update)
	msg_id = get_msg_id(Update)
	user_id = get_user_id(Update)
	chat_id = get_chat_id(Update)
	last_msg_id = msg_id
	text_tok = text.split(" ")
	if text_tok[0] == "/last5":
		if len(text_tok) > 2:
			Bot.sendMessage(user_id, get_team_score(text_tok[1] + " " + text_tok[2]))
			return
		elif len(text_tok) > 1:
			Bot.sendMessage(user_id, "近況:\n"+get_team_score(text_tok[1]))
			return
		else:
			Bot.sendMessage(user_id, "Hello")
			return
	elif text == "/whatsmyip":
		Bot.sendMessage(user_id, "192.168.132.1")
		return
	print(msg_id, text)

def main():
	global last_msg_id
	Updates = Bot.getUpdates(timeout=100)
	if len(Updates) > 0:
		last_msg_id = Updates[-1]["update_id"]

	while(1):
		Updates = Bot.getUpdates(offset=last_msg_id, timeout=100)
		Updates = [Update for Update in Updates if Update["update_id"] > last_msg_id]
		for Update in Updates:
			msg_handler(Update)
		sleep(0.5)
    
if __name__ == "__main__":
    main()


