import paho.mqtt.client as mqtt
import json
import gpiozero
import time

#variabili globali
base = gpiozero.Servo(4)
gripper = gpiozero.Servo(10)
elbow = gpiozero.Servo(17)
shoulder = gpiozero.Servo(22)

min = -1
max = 1

#facilito la ricerca della parte del braccio da muovere
parts = {
	"base": base,
	"gripper": gripper,
	"elbow": elbow,
	"shoulder": shoulder
}

def on_connect(client, userdata, flags, rc):
	print("Connesso al broker con codice {}".format(str(rc)))

	#mi iscrivo al topic del braccio
	client.subscribe("meArm")
	print("Iscritto al topic meArm")

def on_message(client, userdata, msg):
	#print("Topic: {}, messaggio: {}".format(msg.topic, msg.payload.decode("UTF-8")))

	#leggo messaggio con json per comodita
	json_msg = json.loads(msg.payload.decode("UTF-8"))
	print("Da muovere: {}".format(json_msg["part"]))
	print("Valore angolo: {}".format(json_msg["value"]))

	part = json_msg["part"]
	value = json_msg["value"]

	status = move_arm(part, value)
	if status != 0:
		client.publish("meArm_response", "movimento non effettuato")
	else:
		#pubblico risposta di avvenuto movimento
		client.publish("meArm_response", "movimento effettuato")


def move_arm(part, value):

	global parts
	global min
	global max

	if value > max or value < min:
		return -1

	parts[part].value = value
	return 0


#main
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

server_ip_address = "127.0.0.1"
port = 1883

client.connect(server_ip_address, port)

client.loop_forever()
