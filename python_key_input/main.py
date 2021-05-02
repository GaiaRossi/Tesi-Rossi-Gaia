import gpiozero
import time
import keyboard

running = True

pressed = ""

base = gpiozero.Servo(4)
gripper = gpiozero.Servo(10)
elbow = gpiozero.Servo(17)
shoulder = gpiozero.Servo(22)

base_angle = 0
gripper_angle = 0
elbow_angle = 0
shoulder_angle = 0

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

def move_arm_base():

	global base_angle
	global step
	global min
	global max
	global running
	global pressed

	if pressed == "a":
		base_angle = base_angle - step
		if base_angle <= min:
			base_angle = min
		base.value = base_angle
		pressed = ""

	if pressed == "d":
		base_angle = base_angle + step
		if base_angle >= max:
			base_angle = max
		base.value = base_angle
		pressed = ""

def move_arm_gripper():
	global gripper_angle
	global step
	global min
	global max
	global running
	global pressed

	if pressed == "o":
		gripper_angle = gripper_angle + step
		if gripper_angle >= max:
			gripper_angle = max
		gripper.value = gripper_angle
		pressed = ""

	if pressed == "p":
		gripper_angle = gripper_angle - step
		if gripper_angle <= min:
			gripper_angle = min
		gripper.value = gripper_angle
		pressed = ""

def move_arm_elbow():
	global elbow_angle
	global step
	global min
	global max
	global running
	global pressed

	if pressed == "w":
		elbow_angle = elbow_angle + step
		if elbow_angle >= max:
			elbow_angle = max
		elbow.value = elbow_angle
		pressed = ""

	if pressed == "s":
		elbow_angle = elbow_angle - step
		if elbow_angle <= min:
			elbow_angle = min
		elbow.value = elbow_angle
		pressed = ""

def move_arm_shoulder():
	global shoulder_angle
	global step
	global min
	global max
	global running
	global pressed

	if pressed == "j":
		shoulder_angle = shoulder_angle + step
		if shoulder_angle >= max:
			shoulder_angle = max
		shoulder.value = shoulder_angle
		pressed = ""

	if pressed == "l":
		shoulder_angle = shoulder_angle - step
		if shoulder_angle <= min:
			shoulder_angle = min
		shoulder.value = shoulder_angle
		pressed = ""

def may_quit():
	global pressed
	global running

	if pressed == "x":
		running = False


keyboard.on_press(on_press)

while running:
	move_arm_base()
	move_arm_gripper()
	move_arm_elbow()
	move_arm_shoulder()
	may_quit()
