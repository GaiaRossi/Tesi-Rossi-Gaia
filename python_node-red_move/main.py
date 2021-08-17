from gpiozero.pins.pigpio import PiGPIOFactory
import paho.mqtt.client as mqtt
import json
import gpiozero
import time

class Arm():
	def __init__(self, base, gripper, elbow, shoulder):
		self.base = base
		self.gripper = gripper
		self.elbow = elbow
		self.shoulder = shoulder

		self.parts = {
			"base": self.base,
			"gripper": self.gripper,
			"elbow": self.elbow,
			"shoulder": self.shoulder
		}

		self.MIN_VALUE = -1
		self.MAX_VALUE = 1
		self.STEP = 0.01
		self.sensitivity = 0.01

		self.multiplier = 1
		self.is_idle = True

	def move(self, part_name, value):
		if value <= self.MIN_VALUE or value >= self.MAX_VALUE:
			return -1

		self.is_idle = False
		#se il valore in cui mi trovo adesso
		#e piu grande di quello che devo assumere
		#allora dovro diminuire, altrimenti aumentare
		if self.parts[part_name].value > value:
			self.multiplier = -1
		else:
			self.multiplier = 1
		while not (self.parts[part_name].value > value - self.sensitivity and self.parts[part_name].value < value + self.sensitivity):
			self.parts[part_name].value = self.parts[part_name].value + self.multiplier*self.STEP
			print(self.parts[part_name].value)
			#time.sleep(0.3)

		self.is_idle = True
		return 0

#variabili globali
base = gpiozero.Servo(4, pin_factory = PiGPIOFactory())
gripper = gpiozero.Servo(10, pin_factory = PiGPIOFactory())
elbow = gpiozero.Servo(17, pin_factory = PiGPIOFactory())
shoulder = gpiozero.Servo(22, pin_factory = PiGPIOFactory())

arm = Arm(base, gripper, elbow, shoulder)

def on_connect(client, userdata, flags, rc):
	print("Connesso al broker con codice {}".format(str(rc)))

	#mi iscrivo al topic del braccio
	client.subscribe("meArm")
	print("Iscritto al topic meArm")

def on_message(client, userdata, msg):

	global arm

	#print("Topic: {}, messaggio: {}".format(msg.topic, msg.payload.decode("UTF-8")))

	#leggo messaggio con json per comodita
	json_msg = json.loads(msg.payload.decode("UTF-8"))
	values = {
		"base": json_msg["base"],
		"gripper": json_msg["gripper"],
		"elbow": json_msg["elbow"],
		"shoulder": json_msg["shoulder"]
	}

	for part_name, part  in arm.parts.items():
		status = arm.move(part_name, values[part_name])


#main
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

server_ip_address = "127.0.0.1"
port = 1883

client.connect(server_ip_address, port)

try:
	client.loop_forever()
except KeyboardInterrupt:
	print("Disconnessione")
	client.disconnect()
	exit(0)
