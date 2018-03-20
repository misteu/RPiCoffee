from time import sleep, gmtime, strftime
from flask import Flask, request, jsonify, url_for, send_from_directory, send_file, render_template
import requests, datetime
# to read last line of file
from subprocess import check_output
from pymongo import MongoClient

# Define IP and port for Flask-server
HOST = '0.0.0.0'
PORT = 8000

rpiMode = bool(True)

print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

# to mongoDB
client = MongoClient()
client = MongoClient('localhost', 27017)

# define a database at mongoDB
db = client.rpiDB

# define collection inside rpiDB
coffee = db.coffee
rpiIP = "http://0.0.0.0:8000/"

# define debug Messages
message = {}
message["onOff"] = "Maschine faehrt hoch oder runter!"
message["espressoX1"] = "Einfacher Espresso im Bau!"
message["espressoX2"] = "Doppelter Espresso im Bau!"
message["steam"] = "Dampfmaschine am Laden!"
message["clean"] = "Saeuberung gestartet!"
message["coffeeX2"] = "Doppelter Kaffee im Bau"
message["coffeeX1"] = "Einfacher Kaffee im Bau"


if rpiMode:
	from gpiozero import LED
	PORT = 80

	rpiIP = "http://192.168.178.37:80/"

	# Define Espresso outputs as dictionary
	outputs = {}

	# GPIO 10 is currently not used

	# Turn machine on/off: blue wires
	outputs["onOff"] = LED(26)

	# Single espresso: white wires
	outputs["espressoX1"] = LED(19)

	# Prepare steam: yellow wires
	outputs["steam"] = LED(9)

	# Run clean program: gray wires
	outputs["clean"] = LED(11)
	
	# Double coffee: green wires
	outputs["coffeeX2"] = LED(12)

	# Single coffee: orange wires
	outputs["coffeeX1"] = LED(21)

	# Double espresso: violet wires
	outputs["espressoX2"] = LED(13)

def writeDB(data):
	coffee = db.coffeeCollection
	result = coffee.insert_one(data).inserted_id
	return result

def readDB():
	coffee = db.coffeeCollection
	result = []
	for action in coffee.find():
		#action['time'] = strftime("%a, %d %b %Y %H:%M:%S", action['time'])
		result.append(action)
	return result


def readAPIKeys():

	key = {}
	
	# Open a file
	file = open("apiKey.txt", "r")
	key['hafas'] = file.readline().rstrip('\n')
	key['suprnova'] = file.readline().rstrip('\n')
	key['suprnovaId'] = file.readline().rstrip('\n')
	file.close()
	print key
	return key

apiKeys = readAPIKeys()

apiKey_hafas = apiKeys['hafas']
apiKey_suprnova = apiKeys['suprnova']
apiId_suprnova = apiKeys['suprnovaId']


def getWeather():
	r = requests.get('https://www.metaweather.com/api/location/638242/')

	data = r.json()['consolidated_weather']

	return data


def getNextTrains():

	trains = []
# https://www.programmableweb.com/api/berlin-public-transport-rest
# Station S+U Lichtenberg, next Station = Noeldner Platz, show three results

	r = requests.get('https://2.vbb.transport.rest/stations/900000160004/departures?nextStation=900000160003&results=5')
	data = r.json()

	# Schnellere API --> Testen
	# r = request.get('http://demo.hafas.de/openapi/vbb-proxy/departureBoard?id=900160004&accessId=coffee-PI-a570-1cea30e08e6f&format=json')


#print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

	for train in data:

		hour = train['when'].split("T")[1].split(":")[0]
		minute = train['when'].split("T")[1].split(":")[1]

		trains.append(
			{
			"direction":train['direction'],
			"line":train['line']['name'],
			"departure":"{}:{}".format(hour,minute)
			})

	return trains


def getNextTrainsHafas(lines, directions, length):

	lengthCount = 0
	trains = []
	r = requests.get('http://demo.hafas.de/openapi/vbb-proxy/departureBoard?id=900160004&accessId={}&format=json'.format(apiKey_hafas))
	data = r.json()['Departure']

	print('getNextTrainsHafas')
	for train in data:
		if train['Product']['line'] in lines and train['direction'] in directions:
			print(train['rtTime'], train['Product']['line'], train['direction'])

			trains.append(
			{
			"direction":train['direction'],
			"line":train['Product']['line'],
			"departure":train['rtTime']
			})
			lengthCount += 1

		if lengthCount >= length:
			break

	return trains


def getClientName(clientIPStr):

	clientIP = clientIPStr.split(".")
	
	clientIP = int(clientIP[3])

	if (clientIP == 42) or (clientIP == 47):
		print("e")
		name = "Eike"

	elif (clientIP == 23) or (clientIP == 46) or (clientIP == 36):
		print("m")
		name = "Michael"

	else:
		print("guest")
		name = "Gast"

	return name



app = Flask(__name__)



# Rendering UI at GET-Method
@app.route("/", methods=['GET'])
def renderUi():

	weather = getWeather()

	weatherIcon1 = weather[0]['weather_state_abbr']
	weatherIcon2 = weather[1]['weather_state_abbr']
	weatherIcon3 = weather[2]['weather_state_abbr']

	tempMinMax1 = "{}/{}".format(round(weather[0]['min_temp'],1),round(weather[0]['max_temp'],1))
	tempMinMax2 = "{}/{}".format(round(weather[1]['min_temp'],1),round(weather[1]['max_temp'],1))
	tempMinMax3 = "{}/{}".format(round(weather[2]['min_temp'],1),round(weather[2]['max_temp'],1))

	hashrate = 0
	status = ""
	price_usd = 0
	display_trains = "none"
	display_mining = "none"
	display_stats = "none"
	# balanceConf = 0
	# balanceUnconf = 0
	# balanceConfEUR = 0
	# balanceUnconfEUR = 0
	price_eur = 0
	creditEUR = 0
	credit = 0
	trains = []
	strompreisRPiTagEUR = 0
	arbeitspreis = 0
	greeting = bool(True)
	showMore = bool(False)
	stats = {}


	try:
		clientIP = request.remote_addr
		print(clientIP)
		name = getClientName(clientIP)

	except:
		print("could not read remote IP")


	## request Mining stats
	try:

	
		headline = "Guten Morgen {}".format(name)


		request.args['infos']
		if request.args['infos'] == "show":

			
			# Alternativer (langsamer) API-Call
			# trains=getNextTrains()

			try:
				mining = bool(False)
				request.args['mining']
				if request.args['mining'] == "show":
					mining = bool(True)
			except:

				try:
					request.args['showMore']
					if request.args['showMore'] == "true":
						length = 100
						showMore = bool(True)
				except:
					length = 5
					showMore = bool(False)

				lines = ["S5","S7","S75"]
				directions = ["S Westkreuz (Berlin)", "S Westkreuz (Berlin)", "S Potsdam Hauptbahnhof","S Ostkreuz Bhf (Berlin)"]
				trains = getNextTrainsHafas(lines, directions, length)


			if mining:
				r = requests.get('https://xmg.suprnova.cc/index.php?page=api&action=getuserstatus&api_key={}&id={}'.format(apiKey_suprnova, apiId_suprnova))
				validShares = r.json()['getuserstatus']['data']['shares']['valid']
				hashrate = r.json()['getuserstatus']['data']['hashrate']
				sharerate = r.json()['getuserstatus']['data']['sharerate']
				status = check_output(['tail', '-1', '../miner.out'])
				headline = "Mining Informationen"

				#
				# rBalance = requests.get('https://xmg.suprnova.cc/index.php?page=api&action=getuserbalance&api_key=42c6d4df6c897e7bc0fc33e0f8315ad3c7775aa5f701e4d5d9ef0eb823547b99&id=201792128')
				# balanceConf = rBalance.json()['getuserbalance']['data']['confirmed']
				# balanceUnconf = rBalance.json()['getuserbalance']['data']['unconfirmed']
				# 

				rCredit = requests.get('https://xmg.suprnova.cc/index.php?page=api&action=getusertransactions&api_key={}&id={}'.format(apiKey_suprnova, apiId_suprnova))
				credit = rCredit.json()['getusertransactions']['data']['transactionsummary']['Credit']


				r2 = requests.get('https://api.coinmarketcap.com/v1/ticker/magi/?convert=EUR')
				price_eur = r2.json()[0]['price_eur']

				#
				# balanceConfEUR = float(balanceConf) * float(price_eur)
				# balanceUnconfEUR = float(balanceUnconf) * float(price_eur)
				#
				creditEUR = float(credit) * float(price_eur)

				## Kontostand Exponentialformat in Dezimal umwandeln
				# balanceConf = '{0:.6f}'.format(balanceConf)
				# balanceUnconf = '{0:.6f}'.format(balanceUnconf)
				# balanceConfEUR = '{0:.6f}'.format(balanceConfEUR)
				# balanceUnconfEUR = '{0:.6f}'.format(balanceUnconfEUR)

				print(validShares, hashrate, sharerate, status, price_eur, creditEUR)
				display_mining = "block"
				display_trains = "none"
				arbeitspreis = 25.67
				strompreisRPiTagEUR = str(1.04*24*0.001*arbeitspreis*0.01)

			else:
				hashrate = 0
				status = ""
				price_usd = 0
				# balanceConf = 0
				# balanceUnconf = 0
				# balanceConfEUR = 0
				# balanceUnconfEUR = 0
				price_eur = 0
				creditEUR = 0
				credit = 0
				display_trains = "block"
				display_mining = "none"
				greeting = bool(False)
	except:
		print("home-Route")
		# hashrate = 0
		# status = ""
		# price_usd = 0
		# display_trains = "none"
		# display_mining = "none"
		# # balanceConf = 0
		# # balanceUnconf = 0
		# # balanceConfEUR = 0
		# # balanceUnconfEUR = 0
		# price_eur = 0
		# creditEUR = 0
		# credit = 0
		# trains = []
		# strompreisRPiTagEUR = 0
		# arbeitspreis = 0
		# greeting = bool(True)

	# Strompreis bei Strommanufaktur


	try: 
		request.args['stats']
		if request.args['stats'] == "show":
			print("is da!")
			stats = readDB()
			display_stats = "block"
	except:
		print("home-Route")


	return render_template('index.html', stats=stats, display_stats=display_stats, rpiIP=rpiIP, tempMinMax1=tempMinMax1, tempMinMax2=tempMinMax2, tempMinMax3=tempMinMax3, weatherIcon1=weatherIcon1, weatherIcon2=weatherIcon2, weatherIcon3=weatherIcon3, showMore=showMore, greeting=greeting, display_trains=display_trains, display_mining=display_mining, trains=trains, headline=headline, hashrate=hashrate, status=status, price_eur=price_eur, creditEUR=creditEUR, credit=credit, strompreisRPiTagEUR=strompreisRPiTagEUR, arbeitspreis=arbeitspreis)

@app.route("/", methods=['POST'])
def controlMachine():

	# possible actions = dictionary-keys

	action = request.form['action']
	print("Action: {}".format(action))

	if rpiMode:
		# press button
		outputs[str(action)].on()

		# hold button for 500ms
		sleep(0.2)

		# release button
		outputs[str(action)].off()

	clientIP = request.remote_addr
	print(clientIP)
	name = getClientName(clientIP)

	timestamp = gmtime()
	data = {
	"action":action, 
	"time":datetime.datetime(timestamp[0],timestamp[1],timestamp[2],timestamp[3],timestamp[4],timestamp[5]),
	#"time": gmtime(), 
	"username":name, 
	"userip":clientIP
	}

	# writesDB and returns objectID
	print(data)
	print("\n")
	print(writeDB(data))

	return str(message[str(action)])

# Start des Flask-Webservers (muss IMMER in der letzten Zeile stehen!)
app.run(host=HOST,port=PORT)