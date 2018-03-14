from time import sleep, gmtime, strftime
from flask import Flask, request, jsonify, url_for, send_from_directory, send_file, render_template
import requests
from subprocess import check_output

# Define IP and port for Flask-server
HOST = '0.0.0.0'
PORT = 80

rpiMode = bool(True)


print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))


if rpiMode:
	from gpiozero import LED

	# Define Espresso outputs as dictionary
	outputs = {}
	message = {}

	# GPIO 10 is currently not used

	# Turn machine on/off: blue wires
	outputs["onOff"] = LED(26)
	message["onOff"] = "Maschine faehrt hoch oder runter!"

	# Single espresso: white wires
	outputs["espressoX1"] = LED(19)
	message["espressoX1"] = "Einfacher Espresso im Bau!"

	# Prepare steam: yellow wires
	outputs["steam"] = LED(9)
	message["steam"] = "Dampfmaschine am Laden!"

	# Run clean program: gray wires
	outputs["clean"] = LED(11)
	message["clean"] = "Saeuberung gestartet!"

	# Double coffee: green wires
	outputs["coffeeX2"] = LED(12)
	message["coffeeX2"] = "Doppelter Kaffee im Bau"

	# Single coffee: orange wires
	outputs["coffeeX1"] = LED(21)
	message["coffeeX1"] = "Einfacher Kaffee im Bau"

	# Double espresso: violet wires
	outputs["espressoX2"] = LED(13)
	message["espressoX2"] = "Doppelter Espresso im Bau!"


app = Flask(__name__)

# Rendering UI at GET-Method
@app.route("/", methods=['GET'])
def renderUi():

	## request Mining stats
	try:
		request.args['minerInfos']
		if request.args['minerInfos'] == "show":
			r = requests.get('https://xmg.suprnova.cc/index.php?page=api&action=getuserstatus&api_key=42c6d4df6c897e7bc0fc33e0f8315ad3c7775aa5f701e4d5d9ef0eb823547b99&id=201792128')
			validShares = r.json()['getuserstatus']['data']['shares']['valid']
			hashrate = r.json()['getuserstatus']['data']['hashrate']
			sharerate = r.json()['getuserstatus']['data']['sharerate']
			status = check_output(['tail', '-1', '../miner.out'])

			rBalance = requests.get('https://xmg.suprnova.cc/index.php?page=api&action=getuserbalance&api_key=42c6d4df6c897e7bc0fc33e0f8315ad3c7775aa5f701e4d5d9ef0eb823547b99&id=201792128')
			balanceConf = rBalance.json()['getuserbalance']['data']['confirmed']
			balanceUnconf = rBalance.json()['getuserbalance']['data']['unconfirmed']


			r2 = requests.get('https://api.coinmarketcap.com/v1/ticker/magi/?convert=EUR')
			price_eur = r2.json()[0]['price_eur']

			balanceConfEUR = float(balanceConf) * float(price_eur)
			balanceUnconfEUR = float(balanceUnconf) * float(price_eur)

			## Kontostand Exponentialformat in Dezimal umwandeln
			balanceConf = '{0:.6f}'.format(balanceConf)
			balanceUnconf = '{0:.6f}'.format(balanceUnconf)
			balanceConfEUR = '{0:.6f}'.format(balanceConfEUR)
			balanceUnconfEUR = '{0:.6f}'.format(balanceUnconfEUR)

			print(validShares, hashrate, sharerate, status, balanceConf, balanceUnconf)
			display = "block"
	except:

		hashrate = 0
		status = ""
		price_usd = 0
		display = "none"
		balanceConf = 0
		balanceUnconf = 0
		balanceConfEUR = 0
		balanceUnconfEUR = 0
		price_eur = 0

	# Strompreis bei Strommanufaktur
	arbeitspreis = 25.67
	strompreisRPiTagEUR = str(1.04*24*0.001*arbeitspreis*0.01)
	return render_template('index.html', hashrate=hashrate, status=status, price_eur=price_eur, display=display, balanceConf=balanceConf, balanceUnconf=balanceUnconf, balanceConfEUR=balanceConfEUR, balanceUnconfEUR=balanceUnconfEUR, strompreisRPiTagEUR=strompreisRPiTagEUR, arbeitspreis=arbeitspreis)

@app.route("/", methods=['POST'])
def controlMachine():

	# possible actions = dictionary-keys

	action = request.form['action']
	print("Action: {}".format(action))

	# press button
	outputs[str(action)].on()

	# hold button for 500ms
	sleep(0.2)

	# release button
	outputs[str(action)].off()

	return str(message[str(action)])

# Start des Flask-Webservers (muss IMMER in der letzten Zeile stehen!)
app.run(host=HOST,port=PORT)