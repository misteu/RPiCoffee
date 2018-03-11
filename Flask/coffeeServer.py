from time import sleep, gmtime, strftime
from flask import Flask, request, jsonify, url_for, send_from_directory, send_file, render_template

# Define IP and port for Flask-server
HOST = '0.0.0.0'
PORT = 8000

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
	message["clean"] = "Saeuberungsprogramm gestartet!"

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

	return render_template('index.html')

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