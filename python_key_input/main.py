import gpiozero
import time
import keyboard

running = True

pressed = ""

base = gpiozero.Servo(4)

angle = 0
step = 0.1

max = 1
min = -1

def sentinel():
	base.min()
	time.sleep(1)
	base.mid()
	time.sleep(1)
	base.max()
	time.sleep(1)
	base.mid()
	time.sleep(1)

def slow_movement():
	i = i + step
	if i >= max:
		i = max
		step = -step

	if i <= min:
		i = min
		step = -step

	base.value = i
	time.sleep(1) 

def on_press(key):
	global pressed
	pressed = key.name

def move_arm():

	global angle
	global step
	global min
	global max
	global running
	global pressed

	if pressed == "a":
		angle = angle - step
		if angle <= min:
			angle = min
		base.value = angle
		pressed = ""
		time.sleep(0.5)

	if pressed == "d":
		angle = angle + step
		if angle >= max:
			angle = max
		base.value = angle
		pressed = ""
		time.sleep(0.5)

	if pressed == "x":
		running = False


keyboard.on_press(on_press)

while running:
	move_arm()
